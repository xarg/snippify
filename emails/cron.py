#!/usr/bin/python
# coding: utf-8

import sys, os
sys.path.append('/home/sasha/django')

from django.core.management import setup_environ
import snippify.settings
setup_environ(snippify.settings)

from django.core.mail import send_mass_mail, mail_admins

from snippify.emails.models import EmailQueue
from snippify.utils import lock, unlock

def main():
	if lock(): # Acquire lock by creating a temporary directory
		try:
			mass = []
			delete_queues = []
			email_queues = EmailQueue.objects.all()
			for queue in email_queues:
				delete_queues.append(queue.pk)
				mass.append((queue.mail_subject, queue.mail_body, queue.mail_from, [queue.mail_to]))
			send_mass_mail(tuple(mass))
			EmailQueue.objects.filter(pk__in=delete_queues).delete()
		except:
			mail_admins("snippify.me CRON", "Check it out")
		unlock() # Release lock by deleting that directory
if __name__ == "__main__":
	main()