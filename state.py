import _confd
import confd
from confd import dp

class PlatformStateHandler(dp.DataProvider):
    def get_elem(self, tctx, kp):
        """ Provide state data dynamically """
        if "/components/component/state/oper-status" in str(kp):
            return _confd.Value("ACTIVE")  # Example: return 'ACTIVE' status
        elif "/components/component/state/temperature/instant" in str(kp):
            return _confd.Value(45.3)  # Example: return temperature as 45.3
        else:
            raise confd.ConfDError(confd.ERR_NOEXISTS)

# Register the callback
dctx = dp.init_daemon("platform_state")
dp.register_data_cb(dctx, "/components/component/state", PlatformStateHandler())
dp.register_done(dctx)
dp.start(dctx)
