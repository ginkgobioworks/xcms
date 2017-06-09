#!/usr/bin/env python

import os
import subprocess
from glob import glob

from distutils.cmd import Command
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class InstallXcmsDepsCommand(Command):
  description = 'install XCMS deps'

  user_options = [
    ('xcms-install-dir=', None, 'R library/directory in which to install XCMS deps'),
  ]

  def initialize_options(self):
    self.xcms_install_dir = os.environ.get('XCMS_INSTALL_DIR')

  def finalize_options(self):
    if self.xcms_install_dir and not os.path.isdir(self.xcms_install_dir):
      os.makedirs(self.xcms_install_dir)

  def run(self):
    xcms_install_args = []

    if self.xcms_install_dir:
      xcms_install_args = ['-l', self.xcms_install_dir]

    deps = [fn for fn in glob('xcms-deps/*_R_*.tar.gz') if 'xcms' not in os.path.basename(fn)]
    subprocess.check_call(['R', 'CMD', 'INSTALL'] + xcms_install_args + deps)


class InstallXcmsCommand(Command):
  description = 'install XCMS'

  user_options = [
    ('xcms-install-dir=', None, 'R library/directory in which to install XCMS'),
  ]

  def initialize_options(self):
    self.xcms_install_dir = os.environ.get('XCMS_INSTALL_DIR')

  def finalize_options(self):
    if self.xcms_install_dir and not os.path.isdir(self.xcms_install_dir):
      os.makedirs(self.xcms_install_dir)

  def run(self):
    xcms_install_args = []

    if self.xcms_install_dir:
      xcms_install_args = ['-l', self.xcms_install_dir]

      # Propagate build dir arg to deps install command so deps get installed in the same place
      build_xcms_command_obj = self.distribution.get_command_obj('install_xcms_deps')
      build_xcms_command_obj.xcms_install_dir = self.xcms_install_dir

    self.run_command('install_xcms_deps')
    subprocess.check_call(['R', 'CMD', 'INSTALL', '--no-docs'] + xcms_install_args + ['.'])


class RemoveXcmsCommand(Command):
  description = 'uninstall XCMS'

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    subprocess.check_call(['R', 'CMD', 'REMOVE', 'xcms'])


class InstallCommandWithXcms(install):
  def run(self):
    install.run(self)

    # Install R packages wherever this command is being directed to install to
    install_xcms_command_obj = self.distribution.get_command_obj('install_xcms')
    install_xcms_command_obj.xcms_install_dir = os.path.join(
      self.install_data,
      'lib',
      'R',
      'site-library',
    )
    self.run_command('install_xcms')


class DevelopCommandWithXcms(develop):
  def run(self):
    develop.run(self)

    # Install R packages wherever this command is being directed to install to
    install_xcms_command_obj = self.distribution.get_command_obj('install_xcms')
    install_xcms_command_obj.xcms_install_dir = os.path.join(
      self.install_data,
      'lib',
      'R',
      'site-library',
    )
    self.run_command('install_xcms')


setup(
  name='xcms',
  version='1.39.2+ginkgo4',

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
    'Operating System :: POSIX :: Linux',
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
    'install_xcms': InstallXcmsCommand,
    'install_xcms_deps': InstallXcmsDepsCommand,
    'remove_xcms': RemoveXcmsCommand,
    'install': InstallCommandWithXcms,
    'develop': DevelopCommandWithXcms,
  },

  install_requires=[],
  zip_safe=False,
)
