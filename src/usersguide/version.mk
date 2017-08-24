ROLL	= kvm
NAME	= roll-$(ROLL)-usersguide
RELEASE	= 2
RPM.ARCH = noarch

SUMMARY_COMPATIBLE	= $(VERSION)
SUMMARY_MAINTAINER	= Rocks Group
SUMMARY_ARCHITECTURE	= x86_64

ROLL_REQUIRES		= base kernel os
ROLL_CONFLICTS		= xen

PKGROOT         = /var/www/html/roll-documentation/kvm/$(VERSION)
RPM.FILES	= $(PKGROOT)/*
