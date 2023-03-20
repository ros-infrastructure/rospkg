1.5.0 (2023-03-20)
------------------
- Add ventura in the _osx_codename_map
  - https://github.com/ros-infrastructure/rospkg/pull/256
- Use FdoDetect to identify Raspbian systems
  - https://github.com/ros-infrastructure/rospkg/pull/257
- Report Debian 'rodete' as the current Debian testing codename
  - https://github.com/ros-infrastructure/rospkg/pull/258
- List 'ROS Infrastructure Team' as the package maintainer
  - https://github.com/ros-infrastructure/rospkg/pull/252
- Declare test dependencies in [test] extra
  - https://github.com/ros-infrastructure/rospkg/pull/251
- Declare cov/junit module name
  - https://github.com/ros-infrastructure/rospkg/pull/250

1.4.0 (2022-02-24)
------------------
- Add OS_RASPBIAN definition.
  - https://github.com/ros-infrastructure/rospkg/pull/244
- Add Conda OS detection.
  - https://github.com/ros-infrastructure/rospkg/pull/224
  - Fix syntax error in Conda detector
  - https://github.com/ros-infrastructure/rospkg/pull/249
- Avoid use of deprectated distro.linux_distribution() function.
  - https://github.com/ros-infrastructure/rospkg/pull/248
- Enable tests on python 3.10, bump actions/setup-python version.
  - https://github.com/ros-infrastructure/rospkg/pull/246
- Run tests with pytest instead of nose.
  - https://github.com/ros-infrastructure/rospkg/pull/247
- Drop support for python < 2.6.
  - https://github.com/ros-infrastructure/rospkg/pull/242
- Only add pypi dependency on distro with python >= 3.8.
  - https://github.com/ros-infrastructure/rospkg/pull/245
- Use unittest.mock where possible.
  - https://github.com/ros-infrastructure/rospkg/pull/240
- Update debian codename mapping.
  - https://github.com/ros-infrastructure/rospkg/pull/238
- Refactor CI platforms.
  - https://github.com/ros-infrastructure/rospkg/pull/237
- Fix test for riscv machines.
  - https://github.com/ros-infrastructure/rospkg/pull/234
- Add macOS Monterey to OS detection.
  - https://github.com/ros-infrastructure/rospkg/pull/229
- Remove legacy rosbuild files.
  - https://github.com/ros-infrastructure/rospkg/pull/231
- Add rosversion option to show all ROS package names and their versions.
  - https://github.com/ros-infrastructure/rospkg/pull/221
- Address problems with CI
  - Require PyYAML < 6.0 for Python 2.
  - Drop Travis CI configuration and Python 3.4.
  - Use yaml.safe_load
  - https://github.com/ros-infrastructure/rospkg/pull/228
- Update release distributions.
  - Drop support for EOL Ubuntu distros.
  - Drop support for EOL Debian distros.
  - Add Ubuntu Jammy and Debian Bullseye for python3 releases.
  - https://github.com/ros-infrastructure/rospkg/pull/227
  - https://github.com/ros-infrastructure/rospkg/pull/236
- Return list from ManifestManager.list().
  - https://github.com/ros-infrastructure/rospkg/pull/220

1.3.0 (2021-03-31)
-------------------
- Fix for detecting big sur (and newer) versions of macOS
  - https://github.com/ros-infrastructure/rospkg/pull/216
- Add "opensuse-leap" support to os_detect.py
  - https://github.com/ros-infrastructure/rospkg/pull/218
- Switch RedHat-likes to FdoDetect, add some RHEL clones
  - https://github.com/ros-infrastructure/rospkg/pull/219

1.2.10 (2021-02-04)
-------------------
- Fix CentOS 8.3 detection
  - https://github.com/ros-infrastructure/rospkg/pull/215

1.2.9 (2020-11-12)
------------------
- Add armv8l to tripwire_uname test.
  - https://github.com/ros-infrastructure/rospkg/pull/206
- Add OS detection for Buildroot.
  - https://github.com/ros-infrastructure/rospkg/pull/205
- Add OS detection for EulerOS.
  - https://github.com/ros-infrastructure/rospkg/pull/200
- Use GitHub Actions for rospkg CI.
  - https://github.com/ros-infrastructure/rospkg/pull/212
