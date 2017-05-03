Name-based Access Control Library
---------------------------------

Name-based Access Control (NAC) is an encryption-based access control scheme which provides distributed data sharing. For the NAC technical report, please refer to `TR-0034 <http://named-data.net/wp-content/uploads/2015/11/ndn-0034-nac.pdf>`_.

In NAC library, totally there are five kinds of key being used.

- Content Key (C-KEY) which is a symmetric key used to encrypt content directly.
- Encryption Key (E-KEY) / Decryption Key (D-KEY) which is an asymmetric key pair used to encrypt/decrypt C-KEY.
- Consumer public key / private key which is an asymmetric key pair used to encrypt/decrypt D-KEY.

In NAC library, there are three parties with different functionality.

- Data owner. Data owner generates E-KEY/D-KEY pairs and controls consumers' access rights.
- Data producer. Data producer creates content and produce encrypted data.
- Data consumer. Data consumer fetches data and decrypt data.

Naming Conventions
~~~~~~~~~~~~~~~~~~

**Key naming conventions**: Notice that the consumer public/private key pair is following the NDN key naming convention; the key pair will never be encrypted and encapsulated to data packet.

- C-KEY

  ``/<data_prefix>/C-KEY/<time-slot>``

  An example may be like: ``/alice/health/read/activity/C-KEY/20170101170000``. The name of the C-KEY indicates this C-KEY should be used to encrypt content which is produced in 01/01/2017 5:00 PM to 6:00 PM under prefix ``/alice/health/read/activity``.

- D-KEY

  ``/<data_prefix>/D-KEY/[start-ts]/[end-ts]``

  An example may be like: ``/alice/health/read/activity/D-KEY/20170101160000/20170101180000``. The name of the D-KEY indicates this D-KEY should be used to decrypt C-KEYs whose time slot is in the range of 01/01/2017 4:00 PM to 7:00 PM under prefix ``/alice/health/read/activity``.

- E-KEY

  ``/<data_prefix>/E-KEY/[start-ts]/[end-ts]``

  An example may be like: ``/alice/health/read/activity/E-KEY/20170101160000/20170101180000``.  The name of the E-KEY indicates this E-KEY should be used to encrypt C-KEYs whose time slot is in the range of 01/01/2017 4:00 PM to 7:00 PM under prefix ``/alice/health/read/activity``.

**Data packet naming conventions**

- Data packet containing encrypted content

  ``/<data_name>`` or ``/<data_name>/FOR/<C-KEY name>``

  When the content is covered by multiple C-KEYs, to clarify which C-KEY should be fetched, the data packet should have the latter naming convention.

- Data packet containing encrypted C-KEY

  ``/<C-KEY name>/FOR/<D-KEY name>``

  An example may be like: ``/alice/health/SAMPLE/activity/C-KEY/20150101T090000/FOR/alice/health/READ/activity/E-KEY/20150101T080000/20150101T100000``. The name of the data packet indicates the C-KEY is encrypted by the E-KEY whose name is ``/alice/health/READ/activity/E-KEY/20150101T080000/20150101T100000``.

- Data packet containing encrypted D-KEY

  ``/<D-KEY name>/FOR/<consumer name>``

  An example may be like: ``/alice/health/READ/activity/E-KEY/20150101T080000/20150101T100000/alice/health/member-alice``. The name of the data packet indicates the encrypted D-KEY should be decrypted by the private key of the consumer ``/member-alice``.

- Data packet containing encrypted E-KEY

  ``/<E-KEY name>``

Producer, Consumer and Data Owner Logics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In NAC library, there are three parties with different functionality.

Data Owner
^^^^^^^^^^

The main functionality of data owner.

  * Create E-KEY/D-KEY pairs
  * Grant consumers the access to D-KEYs by encrypting D-KEY with consumer's private key.
  * Publish the E-KEYs
  * Consumer management: adding/removing consumers from the access system
  * Maintain the schedule for each consumer

Example:

  1. Creating data owner.

  Assume the data namespace that the owner controls is ``/prefix/dataType``; the database path for data owner is ``dbDir``; the E-KEY/D-KEY length is ``2048``; the freshness period of data packet carrying the keys is ``1 hour``. Then we have:

  .. code-block:: cpp

    GroupManager manager(Name("prefix"), Name("dataType"), dbDir, 2048, 1);

  The function would create the data owner instance.

  2. Getting E-KEY/D-KEY.

  Assume the data owner want to get the E-KEY/D-KEY for the specific time slot 16:30 04/13/2017. Then we have:

  .. code-block:: cpp

    std::list<Data> result = manager.getGroupKey(TimeStamp(from_iso_string("20170413T163000")));

  The function will generate a list of Data packets. The first data packet is the E-KEY. The other data packets are encrypted D-KEY for each consumer who has access right at that time slot. Each D-KEY data packet is encrypted by corresponding consumer's public key.

  3. Adding/Removing schedules

  In NAC, the access unit is based on time; that is, only when one consumer have the access at one specific time slot, the consumer can get the D-KEY. Therefore on data owner's side, there is a concept of **schedule**. The schedule is like a timetable defining which user can have access at which time.

  Assume the data owner want such a schedule: From 04/10/2017 Mon to 04/14/2017 Fri, the authorized time period is from 09:00 to 13:00 on Mon, Wed, and Fri, but no access from 11:00 to 13:00 on 04/12/2017 Wed. Then we can create a schedule:

  .. code-block:: cpp

    RepetitiveInterval intervalA(from_iso_string("20170410T000000"), from_iso_string("20170414T000000"),
                                 9, 13, 2, RepetitiveInterval::RepeatUnit::DAY);
    RepetitiveInterval intervalB(from_iso_string("20170412T000000"), from_iso_string("20170412T000000"),
                                 11, 13);
    Schedule schedule;
    schedule.addWhiteInterval(intervalA); // white interval grants access rights
    schedule.addBlackInterval(intervalB); // black interval enforces no access

  To add the schedule we created, we first need to name it. Here we name the schedule ``schedule 1`` and then:

  .. code-block:: cpp

    manager.addSchedule("schedule1", schedule);
    manager.deleteSchedule("schedule1");

  4. Adding/Removing authorized consumers

  All the authorized consumer is bound with a schedule. The consumer's access is based on the schedule. Adding/removing consumer is to add/remove consumer's certificate. Assume we have Alice whose certificate is ``/group/member/alice/KEY/123/NDNCERT/123`` (Here we call it ``certAlice``) and Bob whose certificate is ``/group/member/bob/KEY/123/NDNCERT/123`` (Here we call it ``certBob``).

  .. code-block:: cpp

    manager.addMember("schedule1", certAlice);
    manager.addMember("schedule1", certBob);
    manager.removeMember(certAlice.getIdentity());

Data producer
^^^^^^^^^^^^^

The main functionality of data producer.

  * Create C-KEY for each minimum access unit
  * Fetch corresponding E-KEY from data owner
  * For each C-KEY, encrypt C-KEY with E-KEY and publish the encrypted C-KEY
  * Produce content
  * For each piece of content, encrypt content with corresponding C-KEY and publish the encrypted content

Example:

  1. Creating data producer.

  Assume the data producer has the namespace ``/prefix`` and would produce data with name ``/prefix/dataType/[TimeStamp]``; the database for data producer is ``dbDir``; the face through which the producer wants to publish data is ``face``. Then we have:

  .. code-block:: cpp

    Producer producer(prefix, dataType, face, dbDir);

  2. Producing C-KEY.

  To create a C-KEY for a specific time slot which we assume it's 16:00 04/13/2017, we need the code:

  .. code-block:: cpp

    typedef function<void(const std::vector<Data>&)> ProducerEKeyCallback;
    Name contentKeyName = producer.createContentKey(from_iso_string("20170413T160001"), ProducerEKeyCallback());

  Notice that the result, the C-KEY data packets encrypted by the corresponding E-KEYs, would be passed back through callback function.

  3. Producing content.

  To produce an data packet encrypted using the content key corresponding time slot, where we assume it's 16:00 04/13/2017, we need the code:

  .. code-block:: cpp

    uint8_t DATA_CONTENT[] = {0xcb, 0xe5, 0x6a, 0x80, 0x41, 0x24, 0x58, 0x23};
    Data result;
    producer.produce(result, from_iso_string("20170413T160001"), DATA_CONTENT, sizeof(DATA_CONTENT));

Data Consumer
^^^^^^^^^^^^^

The main functionality of data consumer.

  * Fetch encrypted content from data producer
  * Fetch encrypted C-KEY from data producer
  * Fetch encrypted D-KEY from data owner
  * Decrypt encrypted D-KEY with consumer's private key
  * Decrypt encrypted C-KEY with D-KEY
  * Decrypt encrypted content with C-KEY

Example:

  1. Creating data consumer

  Assume the data consumer's identity is ``/group/member/bob`` has access to data with namespace ``/prefix``; the database for data consumer is ``dbDir``; the face through which the consumer wants to send out interests is ``face``. Then we have:

  .. code-block:: cpp

    Consumer consumer(face, Name("prefix"), Name("/group/member/bob"), dbDir);

  2. Consuming data

  When data consumer wants to fetch data packet with name ``/prefix/data``, the code would be like:

  .. code-block:: cpp

    typedef function<void (const Data&, const Buffer&)> ConsumptionCallBack;
    consumer.consume(Name("/prefix/data"), ConsumptionCallback(), ErrorCallback);

  The function would automatically fetch corresponding content data packet, C-KEY data packet, and D-KEY data packet. The decrypted content would be passed back through the ``ConsumptionCallback``.