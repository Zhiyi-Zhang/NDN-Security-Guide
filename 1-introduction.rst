Introduction
============

NDN security including security tools and libraries provides application developers with reliable mechanisms to build up the security for new protocol features, algorithms and applications for NDN. The NDN security mainly involves two parts. The first part is **Signing and authentication**, which includes the packet format design and identity management. The other part are security protocols which are designed taking use of NDN architecture.

Signing and authentication
--------------------------

In TCP/IP, it is endpoints' responsibility for security. In contrast, NDN secures the packets directly from the network layer by requiring the data producer to sign very single data packet [1]_. To sign packets on producer side and authenticate the signature on consumer side properly, in NDN security, there is a key management system which involves three important parts.

- Key.
- Certificate.
- Identity.

**Identity** can be considered as a namespace which maps a entity in NDN. Identity may have one or more **keys** under identity's namespace. For each key, there may be one or more **certificates** associated. More details will be illustrated in section ``Identity, Key and Certificate``.

Security Protocols
------------------

Because the security is built into the packet level directly in network layer in NDN, many security design and system can benefit from the change. In NDN, there are a few protocols now or in plan:

- Name-based Access Control Protocol.
- NDN Certificate Management Protocol.
- Key Bundle Protocol.
- DeLorean Protocol.

In this document, we will first introduce the existing security libraries which includes ndn-cxx security library, name-based access control library, and certificate management library. After that, the existing security tools will be introduced. Projects that are in progress will be covered afterwards. Moreover, the future plan of NDN security is showed in the very last section.