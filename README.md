# fids

The FIDS uses a risk based approach on host-based intrusion detection systems (HIDS) that are based on file system monitoring (FIM).

HIDS have generally gotten slower with increased storage capacitz. This is due to the fact that more data means longer time to calculate hashes. The fids doesn't need to calculate hashes. It is based on the sleuth kit (tsk) and uses file system attributes to find intrusions.
