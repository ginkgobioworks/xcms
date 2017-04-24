#!/usr/bin/env python

import os
import subprocess
from glob import glob

from distutils.cmd import Command
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.sdist import sdist


class InstallXcmsDepsCommand(Command):
  """ Install XCMS deps """

  description = 'install XCMS deps'
  user_options = [
    ('xcms-install-dir=', None, 'R library/directory in which to install XCMS'),
  ]

  def initialize_options(self):
    self.xcms_install_dir = os.environ.get('XCMS_INSTALL_DIR')

  def finalize_options(self):
    if self.xcms_install_dir:
      assert os.path.isdir(self.xcms_install_dir), 'XCMS install path must be a valid directory'

  def run(self):
    xcms_install_args = []

    if self.xcms_install_dir:
      xcms_install_args = ['-l', self.xcms_install_dir]

    deps = [fn for fn in glob('*_*.tar.gz') if 'xcms' not in fn]
    subprocess.check_call(['R', 'CMD', 'INSTALL'] + xcms_install_args + deps)


class BuildXcmsCommand(Command):
  description = 'build XCMS'

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    # Install dependencies
    self.run_command('install_xcms_deps')
    subprocess.check_call(['R', 'CMD', 'build', '--no-build-vignettes', '.'])


class InstallXcmsCommand(Command):
  """ Install XCMS using the Python developer tools """

  description = 'install XCMS'
  user_options = [
    ('xcms-install-dir=', None, 'R library/directory in which to install XCMS'),
  ]

  def initialize_options(self):
    self.xcms_install_dir = os.environ.get('XCMS_INSTALL_DIR')

  def finalize_options(self):
    if self.xcms_install_dir:
      assert os.path.isdir(self.xcms_install_dir), 'XCMS install path must be a valid directory'

  def run(self):
    self.run_command('build_xcms')

    xcms_install_args = []

    if self.xcms_install_dir:
      xcms_install_args = ['-l', self.xcms_install_dir]

    subprocess.check_call(['R', 'CMD', 'INSTALL'] + xcms_install_args + glob('xcms_*.tar.gz'))


class InstallCommandWithXcms(install):
  def run(self):
    self.run_command('install_xcms')
    install.run(self)


class DevelopCommandWithXcms(develop):
  def run(self):
    self.run_command('install_xcms')
    develop.run(self)


class SdistCommandWithXcms(sdist):
  def run(self):
    self.run_command('build_xcms')
    sdist.run(self)


setup(
  name='xcms',
  version='1.39.2+ginkgo2',

  description="Ginkgo Bioworks' forked extensions and fixes to XCMS",
  long_description=open('README.md', 'r').read(),
  url='https://bioconductor.org/packages/release/bioc/html/xcms.html',

  author='XCMS Team, Benjie Chen, Ginkgo Bioworks Test Devs',
  author_email='test-devs@ginkgobioworks.com',

  license='GPL-2.0',

  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: Other Environment',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Other',
    'Programming Language :: R',
    'Programming Language :: C++',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Scientific/Engineering :: Chemistry',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Utilities',
  ],

  packages=[],
  include_package_data=True,

  cmdclass={
    'build_xcms': BuildXcmsCommand,
    'install_xcms': InstallXcmsCommand,
    'install_xcms_deps': InstallXcmsDepsCommand,
    'install': InstallCommandWithXcms,
    'develop': DevelopCommandWithXcms,
    'sdist': SdistCommandWithXcms,
  },

  install_requires=[],
  zip_safe=False,
)
