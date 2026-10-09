# Staging

`library-author` writes here and nowhere else. `library-approver` reads
it. A human records approval with `../scripts/approve_change.py`, which
writes `APPROVAL.json`. `library-release` then applies the change and
consumes the record.

This directory is the only writable path inside the library, enforced by
`../hooks/guard_library_write.py`, which knows the package's files from
the install manifest.
