# sentry-ansible

This is a role to install Sentry (https://sentry.io/welcome/) on CentOS or Debian using Python.
So basically it's https://docs.sentry.io/server/installation/python/ fitted into an Ansible role.

If you don't want / need / can't use docker you can easily go with this. :)

It's my first big role, so it might be slighly lame as I'm self thought (without any good practices).
I would appreciate comments and tips how to improve this role. I might need to create a TODO list too.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

1. A weapon of choice - base system - CentOS or Debian in this case.
2. Redis or Memcached
3. PostgreSQL or MariaDB

### Installing

1. Git clone the role
2. Set the host/ group vars / defaults for your needs
3. Run the role
4. If you are running PostgreSQL you might bump into issuses regarding connectivity to the DB.
My case was changing the pg_hba.conf to:

```
local   all             postgres                                trust  
```

For Debian based systems it's located somwhere around:

```
/etc/postgresql/<version>/main/pg_hba.conf
```

For CentOSlike systems it's located somwhere in:
```
/var/lib/pgsql/data/pg_hba.conf
```

5. Create the DB with:

```
createdb -E utf-8 sentry
```

6. Create the initial schema for the database:

```
 SENTRY_CONF=/etc/sentry/sentry.conf.py sentry upgrade
```

7. On CentOS the initial scripts runs a check for a superuser. On Debian tho you need to run:
```
SENTRY_CONF=/etc/sentry/sentry.conf.py sentry createuser
```


## Running the tests

TODO: Automated tests.
Done: Manual test with installing and running basic config. I'm more than 100% sure I've missed something.


## Authors

* **The Wizard** - *Initial work*


## License

This project is licensed under the WTFPLv2 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thank you sentry for creating this piece of software.
* Thank you dear stackoverflow for helping me out with minor problems.
