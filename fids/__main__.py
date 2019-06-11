from controller import FIDS
from config import Config
import sys

if __name__ == "__main__":
    config = './config.yaml'
    run_timeliner = False
    for arg in sys.argv:
        if arg == '-m':
            run_timeliner = True
        elif arg.startswith('--config='):
            config = arg.split('=')[1]
    print(config)
    print(run_timeliner)
    config = Config(config_file=config)
    fids = FIDS(config)
    if run_timeliner:
        fids.timeline_creation()
    else:
        if config.scan_config is not None:
            fids.scan_system()
        if config.investigator_config is not None:
            fids.evaluate_intrusions()
