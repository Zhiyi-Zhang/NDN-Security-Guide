ndn-cxx Security Libraries
--------------------------

In NDN, all the data packets are supposed to have a signature. The signature will ensure the integrity and enable determination of data provenance, allowing a consumer's trust in data to be decoupled from how or where it is obtained.

Regarding interest packet, cryptographically signed signature is not necessary for most cases. However, sometimes interest packet could also bring sender's authority. E.g., a command interest. In such cases, an interest packet also need to be signed.

Signature
~~~~~~~~~

Data packet signature
^^^^^^^^^^^^^^^^^^^^^

NDN Signature is defined as two consecutive TLV blocks: ``SignatureInfo`` and ``SignatureValue``. The following general considerations about SignatureInfo and SignatureValue blocks that apply for all signature types:

1. ``SignatureInfo`` is **included** in signature calculation and fully describes the signature, signature algorithm, and any other relevant information to obtain parent certificate(s), such as KeyLocator.

2. ``SignatureValue`` is **excluded** from signature calculation and represent actual bits of the signature and any other supporting signature material.

The reason for separating the signature into two separate TLV blocks is to allow efficient signing of a contiguous memory block (e.g., for Data packet this block starts from Name TLV and ends with SignatureInfo TLV).

::

    Signature ::= SignatureInfo
                  SignatureValue

    SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
                        SignatureType
                        KeyLocator?
                        ... (SignatureType-specific TLVs)

    SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH
                        ... (SignatureType-specific TLVs and BYTE+)

* SignatureType

  ::

      SignatureType ::= SIGNATURE-TYPE-TYPE TLV-LENGTH
                          nonNegativeInteger

  This specification defines the following SignatureType values:

  +---------+----------------------------------------+-------------------------------------------------+
  | Value   | Reference                              | Description                                     |
  +=========+========================================+=================================================+
  | 0       | :ref:`DigestSha256`                    | Integrity protection using SHA-256 digest       |
  +---------+----------------------------------------+-------------------------------------------------+
  | 1       | :ref:`SignatureSha256WithRsa`          | Integrity and provenance protection using       |
  |         |                                        | RSA signature over a SHA-256 digest             |
  +---------+----------------------------------------+-------------------------------------------------+
  | 3       | :ref:`SignatureSha256WithEcdsa`        | Integrity and provenance protection using       |
  |         |                                        | an ECDSA signature over a SHA-256 digest        |
  +---------+----------------------------------------+-------------------------------------------------+
  | 2,5-200 |                                        | reserved for future assignments                 |
  +---------+----------------------------------------+-------------------------------------------------+
  | >200    |                                        | unassigned                                      |
  +---------+----------------------------------------+-------------------------------------------------+

* KeyLocator

  A ``KeyLocator`` specifies either ``Name`` that points to another Data packet containing certificate or public key or ``KeyDigest`` to identify the public key within a specific trust model (the trust model definition is outside the scope of the current specification). Note that although ``KeyLocator`` is defined as an optional field in ``SignatureInfo`` block, some signature types may require presence of it and some require ``KeyLocator`` absence.

  ::

      KeyLocator ::= KEY-LOCATOR-TYPE TLV-LENGTH (Name | KeyDigest)

      KeyDigest ::= KEY-DIGEST-TYPE TLV-LENGTH BYTE+

  The specific definition of the usage of ``Name`` and ``KeyDigest`` options in ``KeyLocator`` field is outside the scope of this specification. Generally, ``Name`` names the Data packet with the corresponding certificate. However, it is up to the specific trust model to define whether this name is a full name of the Data packet or a prefix that can match multiple Data packets. For example, the hierarchical trust model :cite:`testbed-key-management` uses the latter approach, requiring clients to fetch the latest version of the Data packet pointed by the KeyLocator (the latest version of the public key certificate) in order to ensure that the public key was not yet revoked.


Interest packet signature
^^^^^^^^^^^^^^^^^^^^^^^^^

**Signed Interest** is a mechanism to issue an authenticated interest.

The signature of a signed Interest packet is embedded into the last component of the Interest name. The signature covers a continuous block starting from the first name component TLV to the penultimate name component TLV:

::

    +----------+--------+-------------------------------------------------------------------+
    | Interest |Interest| +----+------+--------------------------------------+ +----------+ |
    |Type(0x01)| Length | |Name| Name | +---------+-   -+---------+---------+| | Other    | |
    |          |        | |Type|Length| |Component| ... |Component|Component|| | TLVs ... | |
    |          |        | |    |      | |  TLV 1  |     | TLV n-1 |  TLV n  || | in       | |
    |          |        | |    |      | +---------+-   -+---------+---------+| | Interest | |
    |          |        | +----+------+--------------------------------------+ +----------+ |
    +----------+--------+-------------------------------------------------------------------+
                                       \                          /\        /
                                        -----------  -------------  ---  ---
                                                   \/                  \/
                                        Signed portion of Interest  Signature

More specifically, the SignedInterest is defined to have four additional components:

-  ``<timestamp>``
-  ``<nonce>``
-  ``<SignatureInfo>``
-  ``<SignatureValue>``

For example, for ``/example/interest/name`` name, CommandInterest will be defined as:

::

     /example/interest/name/<timestamp>/<random-value>/<SignatureInfo>/<SignatureValue>
                           \                                                         /
                            -----------------------------  --------------------------
                                                         \/
                                  Additional components of Signed Interest

* Timestamp component (n-3 *th*)

  The value of the n-3 *th* component is the interest's timestamp (in terms of millisecond offset from UTC 1970-01-01 00:00:00) encoded as nonNegativeInteger. The timestamp may be used to protect against replay attack.

* Nonce component (n-2 *th*)

  The value of the n-2 *th* component is random value (encoded as nonNegativeInteger) that adds additional assurances that the interest will be unique.

* SignatureInfo component (n-1 *th*)

The value of the n-1 *th* component is actually a SignatureInfo TLV which is the same as Data packet SignatureInfo.

  ::

      +---------+---------+-------------------+
      |Component|Component| +---------------+ |
      |   Type  |  Length | | SignatureInfo | |
      |         |         | |      TLV      | |
      |         |         | +---------------+ |
      +---------+---------+-------------------+

      |<---------The n-1 th Component-------->|

* SignatureValue component (n *th*)

  The value of the n *th* component is actually a SignatureValue TLV which is the same as Data packet SignatureValue.

  ::

      +---------+---------+--------------------+
      |Component|Component| +----------------+ |
      |   Type  |  Length | | SignatureValue | |
      |         |         | |      TLV       | |
      |         |         | +----------------+ |
      +---------+---------+--------------------+

      |<----------The n th Component---------->|

Supported Signature Type
^^^^^^^^^^^^^^^^^^^^^^^^
.. _SignatureSha256WithRsa:

* SignatureSha256WithRsa

  ``SignatureSha256WithRsa`` is the basic signature algorithm that MUST be supported by any NDN-compliant software. As suggested by the name, it defines an RSA public key signature that is calculated over SHA256 hash of the Name, MetaInfo, Content, and SignatureInfo TLVs.


  ::

      SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
                          SIGNATURE-TYPE-TYPE TLV-LENGTH(=1) 1
                          KeyLocator

      SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH
                           BYTE+(=RSA over SHA256{Name, MetaInfo, Content, SignatureInfo})

  .. note::

    SignatureValue size varies (typically 128 or 256 bytes) depending on the private key length used during the signing process.

  This type of signature ensures strict provenance of a Data packet, provided that the signature verifies and signature issuer is authorized to sign the Data packet. The signature issuer is identified using KeyLocator block in SignatureInfo block of ``SignatureSha256WithRsa``. KeyDigest option in ``KeyLocator`` is defined as SHA256 digest over the DER encoding of the SubjectPublicKeyInfo for an RSA key as defined by `RFC 3279 <http://www.rfc-editor.org/rfc/rfc3279.txt>`_."

  .. note::

      It is application's responsibility to define rules (trust model) of when a specific issuer (KeyLocator) is authorized to sign a specific Data packet. While trust model is outside the scope of the current specification, generally, trust model needs to specify authorization rules between KeyName and Data packet Name, as well as clearly define trust anchor(s). For example, an application can elect to use hierarchical trust model :cite:`testbed-key-management` to ensure Data integrity and provenance.

.. _SignatureSha256WithEcdsa:

* SignatureSha256WithEcdsa

  ``SignatureSha256WithEcdsa`` defines an ECDSA public key signature that is calculated over the SHA256 hash of the Name, MetaInfo, Content, and SignatureInfoTLVs. The signature algorithm is defined in `[RFC5753], Section 2.1 <http://tools.ietf.org/html/rfc5753#section-2.1>`_.

  ::

      SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
                          SIGNATURE-TYPE-TYPE TLV-LENGTH(=1) 3
                          KeyLocator

      SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH
                           BYTE+(=ECDSA over SHA256{Name, MetaInfo, Content, SignatureInfo})

  .. note::

     The SignatureValue size depends on the private key length used during the signing process (about 63 bytes for a 224 bit key).

  This type of signature ensures strict provenance of a Data packet, provided that the signature verifies and the signature issuer is authorized to sign the Data packet. The signature issuer is identified using the KeyLocator block in the SignatureInfo block of the ``SignatureSha256WithEcdsa``. KeyDigest option in ``KeyLocator`` is defined as SHA256 digest over the DER encoding of the SubjectPublicKeyInfo for an EC key as defined by `RFC 5480 <http://www.ietf.org/rfc/rfc5480.txt>`_.

  The value of ``SignatureValue`` of ``SignatureSha256WithEcdsa`` is a DER encoded DSA signature as defined in `Section 2.2.3 in RFC 3279 <http://tools.ietf.org/html/rfc3279#section-2.2.3>`_.

  ::

      Ecdsa-Sig-Value  ::=  SEQUENCE  {
           r     INTEGER,
           s     INTEGER  }

.. _DigestSha256:

* DigestSha256

  ``DigestSha256`` provides no provenance of a Data packet or any kind of guarantee that packet is from the original source. This signature type is intended only for debug purposes and limited circumstances when it is necessary to protect only against unexpected modification during the transmission.

  ``DigestSha256`` is defined as a SHA256 hash of the Name, MetaInfo, Content, and SignatureInfo TLVs:

  ::

      SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH(=3)
                          SIGNATURE-TYPE-TYPE TLV-LENGTH(=1) 0

      SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH(=32)
                           BYTE+(=SHA256{Name, MetaInfo, Content, SignatureInfo})

  Note that ``SignatureInfo`` does not require ``KeyLocator`` field, since there digest calculation and verification does not require any additional information. If ``KeyLocator`` is present in ``SignatureInfo``, it must be ignored.

Identity, Key and Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All keys, certificates and their corresponding identities are managed by ``KeyChain``. There is an hierarchical structure of keys, certificates and identities; In real world, a user may have multiple identities. Each identity contains one or more keys, one of which is set as the default key of the identity. Similarly, each key contains one or more certificates, one of which is set as the default certificate of the key.

The private part which includes symmetric keys, and private keys of the asymmetric key pairs, is stored in a ``Trusted Platform Module (TPM) <SecTpm>`` in ndn-cxx security library. The public part which includes public keys of the asymmetric key pairs, identities, and certificates are managed in the ``Public-key Information Base (PIB) <SecPublicInfo>`` in ndn-cxx.  The most important information managed by PIB is **certificates** of public keys.

Identity
^^^^^^^^

An real world **identity** can be expressed by a namespace.  (e.g., ``/ndn/edu/ucla/cs/zhiyi``, or ``/ndn/edu/ucla/BoelterHall/4805``).

Key
^^^

When talking about a Key in the context of ndn-cxx, a key refers to a symmetric key or the public key of an asymmetric key pair. Regarding the asymmetric key, algorithm RSA and ECDSA are supported. Regarding the symmetric key, algorithm AES is supported.

**Keys** belonging to an identity are named under the identity's namespace, with a unique **KeyId**

::

    /<identity_name>/KEY/[KeyId]

The KeyId is used to identify the key. When creating a key, there are three types of KeyId could be set. Developer could decide which KeyId to be used by setting the KeyParams. KeyParams is one parameter of the key creating interface.

  * user specified KeyId

    The example code is like:

    .. code-block:: cpp

        // create a new RSA key for identity01
        KeyChain keyChain;
        RsaKeyParams params1(name::Component::fromNumber(123));
        keyChain.createKey(identity01, params1);

  * hash value of the key bits

    The example code is like:

    .. code-block:: cpp

        // create a new RSA key for identity02
        KeyChain keyChain;
        RsaKeyParams params2(1024, KeyIdType::SHA256);
        keyChain.createKey(identity02, params2);

  * randomly generated KeyId

    This kind of KeyId is the default choice of KeyParams. The example code is like:

    .. code-block:: cpp

        // create a new RSA key for identity03
        KeyChain keyChain;
        RsaKeyParams params3;
        keyChain.createKey(identity02, params3);

Certificate
^^^^^^^^^^^

A certificate binds a public key to its key name or the corresponding identity.  The signer (or issuer) of a certificate vouches for the binding through its own signature.  With different signers vouching for the binding, a public key may have more than one certificates.

Since signature verification is a common operation in NDN applications, it is
important to define a common certificate format to standardize the public key
authentication procedure.  As every NDN data packet is signed, a data packet
that carries a public key as content is conceptually a certificate.  However,
the specification of a data packet is not sufficient to be the specification of
a common certificate format, as it requires additional components.  For example,
a certificate may follow a specific naming convention and may need to include
validity period, revocation information, etc.  This specification defines
naming and structure of the NDN certificates and is complementary to NDN packet
specification.

::

                              Overview of NDN certificate format
                                 +--------------------------+
                                 |           Name           |
                                 +--------------------------+
                                 |         MetaInfo         |
                                 |+------------------------+|
                                 || ContentType:  KEY(2)   ||
                                 |+------------------------+|
                                 |+------------------------+|
                                 || FreshnessPeriod: >~ 1h ||
                                 |+------------------------+|
                                 +--------------------------+
                                 |          Content         |
                                 |+------------------------+|
                                 ||       Public Key       ||
                                 |+------------------------+|
                                 +--------------------------+
                                 |       SignatureInfo      |
                                 |+------------------------+|
                                 || SignatureType:  ...    ||
                                 || KeyLocator:     ...    ||
                                 || ValidityPeriod: ...    ||
                                 || ...                    ||
                                 |+------------------------+|
                                 +--------------------------+
                                 |       SignatureValue     |
                                 +--------------------------+


::

     CertificateV2 ::= DATA-TLV TLV-LENGTH
                         Name      (= /<NameSpace>/KEY/[KeyId]/[IssuerId]/[Version])
                         MetaInfo  (.ContentType = KEY,
                                    .FreshnessPeriod >~ 1h))
                         Content   (= X509PublicKeyContent)
                         SignatureInfo (= CertificateV2SignatureInfo)
                         SignatureValue

     X509PublicKeyContent ::= CONTENT-TLV TLV-LENGTH
                                BYTE+ (= public key bits in PKCS#8 format)

     CertificateV2SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
                                      SignatureType
                                      KeyLocator
                                      ValidityPeriod
                                      ... optional critical or non-critical extension blocks ...

* Name

  The name of a certificate consists of five parts as shown below:

  ::

      /<SubjectName>/KEY/[KeyId]/[IssuerId]/[Version]

  A certificate name starts with the subject to which a public key is bound.  The following parts include the keyword ``KEY`` component, KeyId, IssuerId, and version components.

  ``Issuer Id`` is an opaque name component to identify issuer of the certificate.  The value is controlled by the certificate issuer and, similar to KeyId, can be an 8-byte random number, SHA-256 digest of the issuer's public key, or a simple numerical identifier.

  For example,

  ::

        /edu/ucla/cs/yingdi/KEY/%03%CD...%F1/%9F%D3...%B7/%FD%d2...%8E
        \_________________/    \___________/ \___________/\___________/
      Certificate Namespace      Key Id       Issuer Id     Version
            (Identity)


* MetaInfo

  The ``ContentType`` of certificate is set to ``KEY`` (2).

  The ``FreshnessPeriod`` of certificate must be explicitly specified.  The recommended value is 1 hour (3,600,000 milliseconds).

* Content

  By default, the content of a certificate is the public key encoded in `X509PublicKey <https://tools.ietf.org/html/rfc5280#section-4.1.2.7>`__ format.

* SignatureInfo

  The SignatureInfo block of a certificate is required to include the ``ValidityPeriod`` field. ``ValidityPeriod`` includes two sub TLV fields: ``NotBefore`` and ``NotAfter``, which carry two UTC time stamps in ISO 8601 compact format (``yyyymmddTHHMMSS``, e.g., "20020131T235959"). ``NotBefore`` indicates when the certificate takes effect while ``NotAfter`` indicates when the certificate expires.

  .. note::

      Using ISO style string is the convention of specifying the validity period of certificate, which has been adopted by many certificate systems, such as X.509, PGP, and DNSSEC.

  ::

      ValidityPeriod ::= VALIDITY-PERIOD-TYPE TLV-LENGTH
                           NotBefore
                           NotAfter

      NotBefore ::= NOT-BEFORE-TYPE TLV-LENGTH
                      BYTE{15}

      NotAfter ::= NOT-AFTER-TYPE TLV-LENGTH
                     BYTE{15}

  For each TLV, the TLV-TYPE codes are assigned as below:

  +---------------------------------------------+-------------------+----------------+
  | TLV-TYPE                                    | Assigned code     | Assigned code  |
  |                                             | (decimal)         | (hexadecimal)  |
  +=============================================+===================+================+
  | ValidityPeriod                              | 253               | 0xFD           |
  +---------------------------------------------+-------------------+----------------+
  | NotBefore                                   | 254               | 0xFE           |
  +---------------------------------------------+-------------------+----------------+
  | NotAfter                                    | 255               | 0xFF           |
  +---------------------------------------------+-------------------+----------------+

* Extensions

  A certificate may optionally carry some extensions in SignatureInfo.  An extension could be either critical or non-critical depends on the TLV-TYPE code convention. A critical extension implies that if a validator cannot recognize or parse the extension, the validator must reject the certificate.  A non-critical extension implies that if a validator cannot recognize or cannot parse the extension, the validator may ignore the extension.

  The TLV-TYPE code range [256, 512) is reserved for extensions.  The last bit of a TLV-TYPE code indicates whether the extension is critical or not: ``1`` for critical while ``0`` for non-critical.  If an extension could be either critical or non-critical, the extension should be allocated with two TLV-TYPE codes which only differ at the last bit.

* Extensions

  We list currently defined extensions:

  +---------------------------------------------+-------------------+----------------+
  | TLV-TYPE                                    | Assigned code     | Assigned code  |
  |                                             | (decimal)         | (hexadecimal)  |
  +=============================================+===================+================+
  | AdditionalDescription (non-critical)        | 258               | 0x0102         |
  +---------------------------------------------+-------------------+----------------+

* AdditionalDescription

  ``AdditionalDescription`` is a non-critical extension that provides additional information about the certificate.  The information is expressed as a set of key-value pairs.  Both key and value are UTF-8 strings, e.g., ``("Organization", "UCLA")``. The issuer of a certificate can specify arbitrary key-value pair to provide additional description about the certificate.

  ::

      AdditionalDescription ::= ADDITIONAL-DESCRIPTION-TYPE TLV-LENGTH
                                  DescriptionEntry+

      DescriptionEntry ::= DESCRIPTION-ENTRY-TYPE TLV-LENGTH
                             DescriptionKey
                             DescriptionValue

      DescriptionKey ::= DESCRIPTION-KEY-TYPE TLV-LENGTH
                           BYTE+

      DescriptionValue ::= DESCRIPTION-VALUE-TYPE TLV-LENGTH
                             BYTE+

  +---------------------------------------------+-------------------+----------------+
  | TLV-TYPE                                    | Assigned code     | Assigned code  |
  |                                             | (decimal)         | (hexadecimal)  |
  +=============================================+===================+================+
  | DescriptionEntry                            | 512               | 0x0200         |
  +---------------------------------------------+-------------------+----------------+
  | DescriptionKey                              | 513               | 0x0201         |
  +---------------------------------------------+-------------------+----------------+
  | DescriptionValue                            | 514               | 0x0202         |
  +---------------------------------------------+-------------------+----------------+

Signature Signing
~~~~~~~~~~~~~~~~~

Although the security library does not have the intelligence to automatically determine
the signing key for each data packet, it still provides a mechanism, called **Default
Signing Settings**, to facilitate signing process. To achieve the automatic signing and validating, the Trust Scheme is designed, which can refer to `TR-0030 <https://named-data.net/wp-content/uploads/2015/06/ndn-0030-2-trust-schema.pdf>`_.

The basic signing process in the security library would be like this: create ``KeyChain``
instance and supply the data packet and signing by ``KeyChain::sign`` method. One can sign a packet with an identity, a key, or a certificate. Also a not strong signature generated by direct hash function is provided in ndn-cxx.

* Signing with identity

  User can use identity to sign a data packet. When signing, Identity object or identity name could be used as parameter. The default key will be used to generate signature. The default certificate of the default key will be used to generate KeyLocator.

  .. code-block:: cpp

      // signing with Identity identity01 whose name is identityName01
      KeyChain keyChain;
      keyChain.sign(dataPacketA, signingByIdentity(identityName01));
      keyChain.sign(dataPacketB, signingByIdentity(identity01));

* Signing with key

  User can use a specific key to sign a data packet. When signing, Key object or key name could be used as parameter. The default certificate of the default key will be used to generate KeyLocator.

  .. code-block:: cpp

      // signing with Key key02 whose name is keyName02
      KeyChain keyChain;
      keyChain.sign(dataPacketA, signingByKey(keyName02));
      keyChain.sign(dataPacketB, signingByKey(key02));

* Signing with certificate

  User can use a specific certificate to sign a data packet. When signing, Certificate object or certificate name could be used as parameter.

  .. code-block:: cpp

      // signing with Key cert03 whose name is certName03
      KeyChain keyChain;
      keyChain.sign(dataPacketA, signingByCertificate(certName03));
      keyChain.sign(dataPacketB, signingByCertificate(cert03));

* Hash signature

  User can directly sign the data packet with SHA256. There is no encryption in the signing process, which means this kind of signature is not strong.

  .. code-block:: cpp

      // signing with SHA256
      KeyChain keyChain;
      keyChain.sign(dataPacketA, signingWithSha256);

The ``KeyChain`` instance will

- construct ``SignatureInfo`` using the signing certificate name;
- look up the corresponding private key in ``TPM <SecTpm>``;
- sign the data packet if the private key exists.

Validation
~~~~~~~~~~

Validating data packet
^^^^^^^^^^^^^^^^^^^^^^

Validating signed interest
^^^^^^^^^^^^^^^^^^^^^^^^^^