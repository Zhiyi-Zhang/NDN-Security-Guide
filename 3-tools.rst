Existing NDN Security Tools
============================

ndn-cxx Security Command Line Tools
-----------------------------------

List Identities/Keys/Certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-list`` or ``ndnsec-ls-identity`` is a tool to display entities stored in **Public Information Base (PIB)**, such as identities, keys, and certificates.

Usage
^^^^^

::

    $ ndnsec-list [-h] [-KkCc]

Description
^^^^^^^^^^^

``ndnsec-list`` lists names of all the entities according to the granularity specified in options (The default granularity is identity). The default entities will be marked with ``*`` in front of their names. For example:

::

    $ ndnsec list
    * /ndn/edu/ucla/cs/yingdi
      /ndn/test/cathy
      /ndn/test/bob
      /ndn/test/alice


Options
^^^^^^^

``-K, -k``
  Display key names for each identity. The key name with ``*`` in front is the default key name of the corresponding identity.

``-C, -c``
  Display certificate names for each key. The certificate name with ``*`` in front is the default certificate name of the corresponding key.

Examples
^^^^^^^^

Display all the key names in PIB.

::

    $ ndnsec-list -k
    * /ndn/edu/ucla/cs/yingdi
      +->* /ndn/edu/ucla/cs/yingdi/KEY/1397247318867
      +->  /ndn/edu/ucla/cs/yingdi/KEY/1393811874052

      /ndn/test/cathy
      +->* /ndn/test/cathy/KEY/1394129695418

      /ndn/test/bob
      +->* /ndn/test/bob/KEY/1394129695308

      /ndn/test/alice
      +->* /ndn/test/alice/KEY/1394129695025

Display all the certificate names in PIB.

::

    $ ndnsec-list -c
    * /ndn/edu/ucla/cs/yingdi
      +->* /ndn/edu/ucla/cs/yingdi/KEY/1397247318867
           +->* /ndn/edu/ucla/cs/yingdi/KEY/KEY/1397247318867/NDNCERT/%00%00%01ERn%1B%BE
      +->  /ndn/edu/ucla/cs/yingdi/KEY/1393811874052
           +->* /ndn/edu/ucla/cs/yingdi/KEY/KEY/1393811874052/NDNCERT/%FD%01D%85%A9a%DD

      /ndn/test/cathy
      +->* /ndn/test/cathy/KEY/1394129695418
           +->* /ndn/test/KEY/cathy/KEY/1394129695418/NDNCERT/%FD%01D%98%9A%F3J

      /ndn/test/bob
      +->* /ndn/test/bob/KEY/1394129695308
           +->* /ndn/test/KEY/bob/KEY/1394129695308/NDNCERT/%FD%01D%98%9A%F2%AE

      /ndn/test/alice
      +->* /ndn/test/alice/KEY/1394129695025
           +->* /ndn/test/KEY/alice/KEY/1394129695025/NDNCERT/%FD%01D%98%9A%F2%3F


Delete Identities/Keys/Certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-delete`` is a tool to delete security data from both **Public Info Base** and **Trusted Platform Module**.

Usage
^^^^^

::

    ndnsec-delete [-h] [-kc] name

Description
^^^^^^^^^^^

By default, ``ndnsec-delete`` interpret ``name`` as an identity name. If an identity is deleted, all the keys and certificates belonging to the identity will be deleted as well. If a key is deleted,  all the certificate belonging to the key will be deleted as well.


Options
^^^^^^^

``-k``
  Interpret ``name`` as a key name and delete the key and its related data.

``-c``
  Interpret ``name`` as a certificate name and delete the certificate.

Exit Status
^^^^^^^^^^^

Normally, the exit status is 0 if the requested entity is deleted successfully. If the entity to be deleted does not exist, the exit status is 1. For other errors, the exit status is 2.

Examples
^^^^^^^^

Delete all data related to an identity:

::

    $ ndnsec-delete /ndn/test/david


Get Default Identities/Keys/Certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-get-default`` is a tool to display the default setting of a particular entity.

Usage
^^^^^

::

    $ ndnsec-get-default [-h] [-kc] [-i identity|-K key] [-q]

Description
^^^^^^^^^^^

Given a particular entity, ``ndnsec-get-default`` can display its default setting as specified in options. If ``identity`` is specified, the given entity becomes the identity. If ``key`` is specified, the given identity becomes the key. If no entity is specified, the command will take the system default identity as the given entity.

Options
^^^^^^^

``-k``
  Display the given entity's default key name.

``-c``
  Display the given entity's default certificate name.

``-i identity``
  Display default setting of the ``identity``

``-K key``
  Display default setting of the ``key``.

``-q``
  Disable trailing new line character.

Examples
^^^^^^^^

Display an identity's default key name.

::

    $ ndnsec-get-default -k -i /ndn/test/alice
    /ndn/test/alice/KEY/1394129695025

Display an identity's default certificate name.

::

    $ ndnsec-get-default -c -i /ndn/test/alice
    /ndn/test/KEY/alice/KEY/1394129695025/NDNCERT/%FD%01D%98%9A%F2%3F

Display a key's default certificate name.

::

    $ ndnsec-get-default -c -K /ndn/test/alice/KEY/1394129695025
    /ndn/test/KEY/alice/KEY/1394129695025/NDNCERT/%FD%01D%98%9A%F2%3F


Set Default Identities/Keys/Certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-set-default`` is a tool to change the default security settings.

Usage
^^^^^

::

    $ ndnsec-set-default [-h] [-k|c] name

Description
^^^^^^^^^^^

By default, ``ndnsec-set-default`` takes ``name`` as an identity name and sets the identity as the
system default identity.

Options
^^^^^^^

``-k``
  Set default key. ``name`` should be a key name, ``ndnsec-set-default`` can infer the corresponding
  identity and set the key as the identity's default key.

``-c``
  Set default certificate. ``name`` should be a certificate name, ``ndnsec-set-default`` can
  infer the corresponding key name and set the certificate as the key's default certificate.

Examples
^^^^^^^^

Set a key's default certificate:

::

    $ ndnsec-set-default -c /ndn/test/KEY/alice/KEY/1394129695025/NDNCERT/%FD%01D%98%9A%F2%3F

Set an identity's default key:

::

    $ ndnsec-set-default -k /ndn/test/alice/KEY/1394129695025

Set system default identity:

::

    $ ndnsec-set-default /ndn/test/alice

Generate a New Key
~~~~~~~~~~~~~~~~~~

``ndnsec-key-gen`` is tool to generate a pair of key.

Usage
^^^^^

::

    $ ndnsec-key-gen [-h] [-n] [-d] [-t keyType] identity

Description
^^^^^^^^^^^

``ndnsec-key-gen`` creates a key pair for the specified ``identity`` and sets the key as the identity's default key. ``ndnsec-key-gen`` will also create a signing request for the generated key. The signing request will be written to standard output in base64 encoding. By default, it will also set the identity as the system default identity.

Options
^^^^^^^

``-n``
  Do not set the identity as the system default identity. Note that if it is the first identity/key/certificate, then it will be set as default regardless of ``-n`` flag.

``-t keyType``
  Specify the key type. ``r`` (default) for RSA key. ``e`` for ECDSA key.

Examples
^^^^^^^^

::

    $ ndnsec-key-gen /ndn/test/zhiyi
    Bv0CwQcyCANuZG4IBHRlc3QIBXpoaXlpCANLRVkICLc7RCqUMJsBCARzZWxmCAn9
    AAABXFeBQmEUCRgBAhkEADbugBX9ASYwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
    ggEKAoIBAQDI+5XnQxL2iIORZ+ijbOF3na/ayDNhmVvy0QY2fpEIG6/u5xaKD0kt
    r+m1P7Ibm1HTF/qdXDrJe++zif0WnGKfaNXH8ZGRej2TU387rUhE0b+RfCij1gaV
    R5WHxB7us++3KsBiRi3s9yrGpRDtWXMjfTl09I6PSLKU57WPmATPSt9RF/24xWVN
    /IiOqzB2aHDtrOO/DMaSe7gtOMANL8bsmu8GiVl9wdLm+UBQe1zDWbA1D19opkyO
    Px7fg8ZNKqsrHIL7WQ/JWR6hoheOup3G5Fl4hByNM4Qkt3JwU3Pwx3+37z550+e+
    HR/MQ1RMDm/4FS52xGqN9UcuAkPq/Q2ZAgMBAAEWUhsBARwjByEIA25kbggEdGVz
    dAgFemhpeWkIA0tFWQgItztEKpQwmwH9AP0m/QD+DzE5NzAwMTAxVDAwMDAwMP0A
    /w8yMDM3MDUyNVQwMzU4MjcX/QEAPyF53NI4lsMBB+maUBsT3DUG5ttgLzgTHIM5
    x4dBJ3gaVqCm34/CqH/XoZDRMYr378fJ8zTjKhv+exgb/LRAkJYBtXmrRZpwafaP
    GHsBQP89baxz48suUeUi6mGOaycCV/VmG+3DDjbqm5Gx+biv5j7jAgH7UsyVE7uU
    eJKvCl117CR/JOG8G4CRc2e8AUg69GAngAAhLSLhdsoiGwg3gSST5K+jUtBDiCk1
    pv+XEiAB/bk6LB/eGzCBtyCZdA44v5Sb6Y/qa1xhcSQKWKIKjHKQt/QU2X4UtL0Y
    OCXnDOjv4zKvRce0YO3aUFuZ6w1ruyfarL1ZHngWpZJyv0CvGg==


Generate a Certificate Request for a Key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-sign-req`` is a tool to generate a signing request for a particular key.

Usage
^^^^^

::

    $ ndnsec-sign-req [-h] [-k] name

Description
^^^^^^^^^^^

The signing request of a key is actually a self-signed certificate. Given key's information, ``ndnsec-sign-req`` looks up the key in PIB. If such a key exists, a self-signed certificate of the key, or its signing request, will be outputed to **stdout** with base64 encoding.

By default, ``name`` is interpreted as an identity name. ``ndnsec-sign-req`` will generate a signing request for the identity's default key.

Options
^^^^^^^

``-k``
  Interpret ``name`` as a key name.

Examples
^^^^^^^^

Create a signing request for an identity's default key.

::

    $ ndnsec-sign-req /ndn/test/zhiyi
    Bv0CyQc6CANuZG4IBHRlc3QIBXpoaXlpCANLRVkICLc7RCqUMJsBCAxjZXJ0LXJl
    cXVlc3QICf0AAAFcV4jHGBQJGAECGQQANu6AFf0BJjCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBAMj7ledDEvaIg5Fn6KNs4Xedr9rIM2GZW/LRBjZ+kQgb
    r+7nFooPSS2v6bU/shubUdMX+p1cOsl777OJ/RacYp9o1cfxkZF6PZNTfzutSETR
    v5F8KKPWBpVHlYfEHu6z77cqwGJGLez3KsalEO1ZcyN9OXT0jo9IspTntY+YBM9K
    31EX/bjFZU38iI6rMHZocO2s478MxpJ7uC04wA0vxuya7waJWX3B0ub5QFB7XMNZ
    sDUPX2imTI4/Ht+Dxk0qqyscgvtZD8lZHqGiF466ncbkWXiEHI0zhCS3cnBTc/DH
    f7fvPnnT574dH8xDVEwOb/gVLnbEao31Ry4CQ+r9DZkCAwEAARZSGwEBHCMHIQgD
    bmRuCAR0ZXN0CAV6aGl5aQgDS0VZCAi3O0QqlDCbAf0A/Sb9AP4PMjAxNzA1MzBU
    MDQwNjQx/QD/DzIwMTcwNjA5VDA0MDY0MBf9AQB7grtVx1PbkUjRumbDREpCpUCl
    iFXtznijlgucAgTgJEBJdE2caFwW1P2pgJmhkvIHCFSqhX3GvIDfpGgoh88rik83
    IAX+gqKjdgsCbrecUAEEHG9HOvOZpfreNBI/a08095n0twHLj2gH3zC+hUJzt/tB
    mfHswAxoi/e0Lfm2FMJzlaC0oNRzDRcnWMYGvvuZ7RNddVhh5rh8QVLnsOxiotNo
    SLNy7QB/+PwHN1/fHXC18ZgIBHcXAVRMy6cgpjJTI5Jn31OEpWtx8v1HJGEefljk
    xHPbRSTylNnqv9apVNTfA6/BlftZWGaipgo6nNLlqKkMyZpM695+ZBrRdLx7


Create a signing request for a particular key.

::

    $ ndnsec-sign-req -k /ndn/test/zhiyi/KEY/%B7%3BD%2A%940%9B%01
    Bv0CyQc6CANuZG4IBHRlc3QIBXpoaXlpCANLRVkICLc7RCqUMJsBCAxjZXJ0LXJl
    cXVlc3QICf0AAAFcV4luAxQJGAECGQQANu6AFf0BJjCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBAMj7ledDEvaIg5Fn6KNs4Xedr9rIM2GZW/LRBjZ+kQgb
    r+7nFooPSS2v6bU/shubUdMX+p1cOsl777OJ/RacYp9o1cfxkZF6PZNTfzutSETR
    v5F8KKPWBpVHlYfEHu6z77cqwGJGLez3KsalEO1ZcyN9OXT0jo9IspTntY+YBM9K
    31EX/bjFZU38iI6rMHZocO2s478MxpJ7uC04wA0vxuya7waJWX3B0ub5QFB7XMNZ
    sDUPX2imTI4/Ht+Dxk0qqyscgvtZD8lZHqGiF466ncbkWXiEHI0zhCS3cnBTc/DH
    f7fvPnnT574dH8xDVEwOb/gVLnbEao31Ry4CQ+r9DZkCAwEAARZSGwEBHCMHIQgD
    bmRuCAR0ZXN0CAV6aGl5aQgDS0VZCAi3O0QqlDCbAf0A/Sb9AP4PMjAxNzA1MzBU
    MDQwNzI0/QD/DzIwMTcwNjA5VDA0MDcyMxf9AQAQE10+dbgLg7FkYEe8T1wRQqJN
    9CJYSPNr1HLg3BqJ+evJjCtHGFk4e87r9HUhMx2JPsL8ldl8q/QzzqSgLuh1L+nm
    Ts2d0Aod15mVOPJpZHsZnuTPemZS0lol0kYkSTi//xFoyrnFCriTiwW7+Lesulnj
    ASoRVZJfyaj/G+O0g5DmrHBwDDUku9x7N6HQMiplK9iFpuWiM7Q5HIjsX/UCkGYD
    em/K1dk8sb8pWVnE6K+o7IBJElqbyriDWPhH08AHnNSsyBr0jRjoCw4fUCBAoiRC
    cWbzI+5gN0eTgmY6msRKofR0HkPwxwWTdLu9KCbXH6nsO/C14GdgvosuliUb

Generate a New Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-cert-gen`` is a tool to issue an identity certificate.

Usage
^^^^^

::

    $ ndnsec-cert-gen [-h] [-S timestamp] [-E timestamp] [-I info] [-s sign-id] [-i issuer-id] request

Description
^^^^^^^^^^^

``ndnsec-cert-gen`` takes signing request as input and issues an identity certificate for the key in the signing request. The signing request can be created during ``ndnsec-keygen`` and can be re-generated with ``ndnsec-sign-req``.

By default, the default key/certificate will be used to sign the issued certificate.

``request`` could be a path to a file that contains the signing request. If ``request`` is ``-``, then signing request will be read from standard input.

The generated certificate will be written to standard output in base64 encoding.

Options
^^^^^^^

``-S timestamp``
  Timestamp when the certificate becomes valid. The default value is now.

``-E timestamp``
  Timestamp when the certificate expires. The default value is one year from now.

``-I info``
  Other information to be included in the issued certificate.  For example,

   ::

      -I "affiliation Some Organization" -I "homepage http://home.page/"

``-s sign-id``
  Signing identity. The default key/certificate of ``sign-id`` will be used to sign the requested
  certificate. If this option is not specified, the system default identity will be used.

``-s issuer-id``
  Issuer's ID to be included as part of the issued certificate name.  If not specified, "NA"
  value will be used

Examples
^^^^^^^^

::

    $ ndnsec-cert-gen -S 20140401000000 -E 20150331235959 -N "David"
    -I "2.5.4.10 'Some Organization'" -s /ndn/test sign_request.cert
    Bv0C9wc9CANuZG4IBHRlc3QIA0tFWQgFZGF2aWQIEWtzay0xMzk2OTEzMDU4MTk2
    CAdJRC1DRVJUCAgAAAFFPp2g3hQDGAECFf0BdjCCAXIwIhgPMjAxNDA0MDEwMDAw
    MDBaGA8yMDE1MDMzMTIzNTk1OVowKDAMBgNVBCkTBURhdmlkMBgGA1UEChMRU29t
    ZSBPcmdhbml6YXRpb24wggEgMA0GCSqGSIb3DQEBAQUAA4IBDQAwggEIAoIBAQC0
    urnS2nKcnXnMTESH2XqO+H8c6bCE6mmv+FMQ9hSfZVOHbX4kkiDmkcAAf8NCvwGr
    kEat0NQIhKHFLFtofC5rXLheAo/UxgFA/9bNwiEjMH/c8EN2YTSMzdCDrK6TwE7B
    623cLTsa3Bb11+BpzC1oLb3Egedgp+vIf+AFIgNQhvfwzsgsgOBB4iJBwcYegU7w
    JsO0pjY69WQU2DGjABFef6C2Qh8x0TvtnynRLbWlh928+4ilVUvLuWcV3AbPIKLe
    eZu13+v01JN6kFzNZDPMFtOFPvJ943IdYu7Q9k93PzhSk0+wFp3cHH21PfWeghWe
    3zLIER8RTWPIQhWSbxRVAgERFjMbAQEcLgcsCANuZG4IA0tFWQgEdGVzdAgRa3Nr
    LTEzOTQxMjk2OTQ3ODgIB0lELUNFUlQX/QEABUGcl7U+F8cwMHKckerv+1H2Nvsd
    OfeqX0+4RzWU+wRx2emMGMZZdHSx8M/i45hb0P5hbNEF99L35/SrSTSzhTZdOriD
    t/LQOcKBoNXY+iw3EUFM0gvRGU0kaEVBKAHtbYhtoHc48QLEyrsVaMqmrjCmpeF/
    JOcClhzJfFW3cZ/SlhcTEayF0ntogYLR2cMzIwQhhSj5L/Kl7I7uxNxZhK1DS98n
    q8oGAxHufEAluPrRpDQfI+jeQ4h/YYKcXPW3Vn7VQAGOqIi6gTlUxrmEbyCDF70E
    xj5t3wfSUmDa1N+hLRMdEAI+IjRRHDSx2Lhj/QcoPIZPWwKjBz9CBL92og==


Dump a Certificate
~~~~~~~~~~~~~~~~~~

``ndnsec-cert-dump`` is a tool to dump a certificate from **Public Info Base** or file and output
it to standard output.

Usage
^^^^^

::

    $ ndnsec-cert-dump [-h] [-p] [-ikf] name

Description
^^^^^^^^^^^

``ndnsec-cert-dump`` can read a certificate from **Public Info Base (PIB)** or a file and output
the certificate to standard output.

By default, ``name`` is interpreted as a certificate name.

Options
^^^^^^^

``-i``
  Interpret ``name`` as an identity name. If specified, the certificate to dump is the default
  certificate of the identity.

``-k``
  Interpret ``name`` as a key name. If specified, the certificate to dump is the default certificate
  of the key.

``-f``
  Interpret ``name`` as a path to a file containing the certificate. If ``name`` is ``-``,
  certificate will be read from standard input.

``-p``
  Print out the certificate to a human-readable format.

Examples
^^^^^^^^

Dump a certificate from PIB to standard output:
::

    $ ndnsec-cert-dump /ndn/test/david/KEY/1396913058196/NDNCERT/%00%00%01E%3E%9D%A0%DE

Dump a certificate to a human-readable format:
::

    $ ndnsec-cert-dump -p /ndn/test/david/KEY/1396913058196/NDNCERT/%00%00%01E%3E%9D%A0%DE
    Certificate name:
      /ndn/test/david/KEY/1396913058196/NDNCERT/%00%00%01E%3E%9D%A0%DE
    Validity:
      NotBefore: 20140401T000000
      NotAfter: 20150331T235959
    Subject Description:
      2.5.4.41: David
      2.5.4.10: Some Organization
    Public key bits:
    MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAtLq50tpynJ15zExEh9l6
    jvh/HOmwhOppr/hTEPYUn2VTh21+JJIg5pHAAH/DQr8Bq5BGrdDUCIShxSxbaHwu
    a1y4XgKP1MYBQP/WzcIhIzB/3PBDdmE0jM3Qg6yuk8BOwett3C07GtwW9dfgacwt
    aC29xIHnYKfryH/gBSIDUIb38M7ILIDgQeIiQcHGHoFO8CbDtKY2OvVkFNgxowAR
    Xn+gtkIfMdE77Z8p0S21pYfdvPuIpVVLy7lnFdwGzyCi3nmbtd/r9NSTepBczWQz
    zBbThT7yfeNyHWLu0PZPdz84UpNPsBad3Bx9tT31noIVnt8yyBEfEU1jyEIVkm8U
    VQIB


Install a New Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-cert-install`` is a tool to install a certificate into **Public Information Base (PIB)**.

Usage
^^^^^

::

    $ ndnsec-cert-install [-h] [-IKN] cert-source

Description
^^^^^^^^^^^

``ndnsec-cert-install`` can insert a certificate into PIB. By default, the installed certificate
will be set as the default certificate of its corresponding identity and the identity is set as
the system default identity.

``cert-source`` could be a filesystem path or an HTTP URL of a file containing to certificate to
install or . If ``cert-file`` is ``-``, the certificate will be read from standard input.

Options
^^^^^^^

``-I``
  Set the certificate as the default certificate of its corresponding identity, but do not change
  the system default identity.

``-K``
  Set the certificate as the default certificate of its corresponding key, but do not change the
  corresponding identity's default key and the system default identity.

``-N``
  Install the certificate but do not change any default settings.

Examples
^^^^^^^^

Install a certificate and set it as the system default certificate:

::

    $ ndnsec-cert-install cert_file.cert

Install a certificate with HTTP URL and set it as the system default certificate:

::

    $ ndnsec-install-cert "http://ndncert.domain.com/cert/get/my-certificate.ndncert"

Install a certificate but do not change any default settings:

::

    $ ndnsec-cert-install -N cert_file.cert

Export Security Data of an identity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-export`` is a tool to export an identity's security data

Usage
^^^^^

::

    $ ndnsec-export [-h] [-o output] [-p] identity

Description
^^^^^^^^^^^

``ndnsec-export`` can export public data of the ``identity`` including default key/certificate.
``ndnsec-export`` can also export sensitive data (such as private key), but the sensitive data will
be encrypted. The exported identity can be imported again using ``ndnsec-import``.

By default, the command will write exported data to standard output.

Options
^^^^^^^

``-o output``
  Output the exported data to a file pointed by ``output``.

``-p``
  Export private key of the identity. A password will be asked for data encryption.

Examples
^^^^^^^^

Export an identity's security data including private key and store the security data in a file:

::

    $ ndnsec-export -o id.info -p /ndn/test/alice

Export an identity's security data without private key and write it to standard output:

::

    $ ndnsec-export /ndn/test/alice


Import Security Data of an identity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ndnsec-import`` is a tool to import an identity's security data that is prepared by ``ndnsec-export``.

Usage
^^^^^

::

    $ ndnsec-import [-h] [-p] input

Description
^^^^^^^^^^^

``ndnsec-import`` read data from ``input``. It will ask for password if the input contains private key. If ``input`` is ``-``, security data will be read from standard input.

Options
^^^^^^^

``-p``
  Indicates the imported data containing private key. A password will be asked for data encryption.

Examples
^^^^^^^^

Import an identity's security data including private key:

::

    $ ndnsec-import -p input_file

Unlock the TPM
~~~~~~~~~~~~~~

``ndnsec-unlock-tpm`` is a tool to (temporarily) unlock the **Trusted Platform Module (TPM)** that
manages private keys.

Usage
^^^^^

::

    $ ndnsec-unlock-tpm [-h]

Description
^^^^^^^^^^^

``ndnsec-unlock-tpm`` will ask for password to unlock the TPM.
