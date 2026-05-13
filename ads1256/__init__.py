"""ADS1256 ROS 2 package.

Keep package import lightweight. Hardware-only dependencies such as pipyadc
must not be imported from here because ROS launch imports the package before
node parameters like simulate:=true can be processed.
"""

__all__ = []
