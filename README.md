I'm having problems running tests on a project with multiple databases. It 
seems that the testcase setup fails before it ever reaches my code, 
because the south_migrationhistory table only exists in one database, but 
South expects to find it in all databases. 

The bug is under discussion on the [South mailing list](https://groups.google.com/forum/?fromgroups=#!topic/south-users/Sre6bO9aJzo).

You can repro this problem using this demo app, like this:

	git clone git@github.com:qris/south-migration-multiple-databases-problem.git
	cd south-migration-multiple-databases-problem
	virtualenv ve
	ve/bin/pip install -r pip_packages.txt
	ve/bin/python migration_multiple_databases_problem/manage.py test app1

This is part of the stack trace leading to the failure: 

	-> failures = test_runner.run_tests(test_labels) 
	   django-1.5/django/test/simple.py(367)run_tests() 
	-> old_config = self.setup_databases() 
	   django-1.5/django/test/simple.py(315)setup_databases() 
	-> self.verbosity, autoclobber=not self.interactive) 
	   ischool_user_manager/.ve/local/lib/python2.7/site-packages/south/hacks/django_1_0.py(100)wrapper() 
	-> f(*args, **kwargs) 
	   django-1.5/django/db/backends/creation.py(293)create_test_db() 
	-> load_initial_data=False) 
	   django-1.5/django/core/management/__init__.py(160)call_command() 
	-> return klass.execute(*args, **defaults) 
	   django-1.5/django/core/management/base.py(252)execute() 
	-> output = self.handle(*args, **options) 
	   django-1.5/django/core/management/base.py(382)handle() 
	-> return self.handle_noargs(**options) 
	   ischool_user_manager/.ve/local/lib/python2.7/site-packages/south/management/commands/syncdb.py(99)handle_noargs() 
	-> management.call_command('migrate', **options) 
	   django-1.5/django/core/management/__init__.py(160)call_command() 
	-> return klass.execute(*args, **defaults) 
	   django-1.5/django/core/management/base.py(252)execute() 
	-> output = self.handle(*args, **options) 
	   ischool_user_manager/.ve/local/lib/python2.7/site-packages/south/management/commands/migrate.py(108)handle() 
	-> ignore_ghosts = ignore_ghosts, 
	> ischool_user_manager/.ve/local/lib/python2.7/site-packages/south/migration/__init__.py(175)migrate_app() 
	-> south.db.db.debug = (verbosity > 1) 

django/test/simple.py:setup_databases() is looping over all databases that 
are not marked as TEST_MIRRORs, in the second pass loop. It calls 
create_test_db() on each one, which calls the syncdb management command, 
which South intercepts in order to call migrate. 

This is doing a query for MigrationHistory objects in the database that's 
currently being created: 

	applied_all = MigrationHistory.objects.filter(applied__isnull=False).order_by('applied').using(database) 

But if the database that we're creating is not the same one that 
MigrationHistory objects are routed to, then this will throw an uncaught 
exception: 

	DatabaseError: no such table: south_migrationhistory 

A workaround in my case is to mark all databases except the default one as 
TEST_MIRRORs. But that won't work for everyone. 

Does anyone know whether MigrationHistory is supposed to be sharded across 
all non-mirror databases? If so, then we have to be careful when writing 
our database routers to allow it to syncdb in all databases, which is not 
intuitive. Perhaps it's the true solution in our case. 

Perhaps it would be helpful if we trap this DatabaseError in South, and 
raise a more helpful exception? 
