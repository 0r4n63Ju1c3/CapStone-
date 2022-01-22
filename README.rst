=============
CapStone-
=============

This is the main repository that we are using for our CapStone project. The goal
of the project is to compare the encryption standard `ASCON`_. The performance
metrics used are listed below. To accurately gauge the the performance, the
performance metric for no encryption and AES are also provided in the repo.

Performance Metrics
-------------------

* Processor usage
* Time
* Power Consumption

Since the precision and difficulty of synchronizing clocks is outside the scope
of this project, round trip time is being measured and divided in half. The
plaintext message is randomly generated beforehand.

The process is as follows:

1. Clock is started
2. Plaintext is encrypted to ciphertext
3. Ciphertext is send to server
4. Server unencrypts ciphertext to plaintext
5. Plaintext is re-encrypted
6. Re-encrypted ciphertext send back to client
7. Client unencrypts to plaintext
8. Plaintext then compared to original message
9. Clock is stopped

*Diagram shown below*

..image:: diagram.png


 .. _ASCON: https://ascon.iaik.tugraz.at/
