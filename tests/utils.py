from contextlib import contextmanager


class SignalsMixin:
    @contextmanager
    def assert_signal_sent(self, signal, expected_sender, **expected_kwargs):
        err = "The expected signal was not called"

        def dispatcher(sender, **kwargs):
            nonlocal err

            if sender != expected_sender:
                err = f"The expected sender {expected_sender} is different from the actual {sender}"
                return

            kwargs.pop("signal")
            if expected_kwargs != kwargs:
                err = f"The expected arguments differ from the actual ones: {expected_kwargs} != {kwargs}"
                return

            err = ""

        try:
            signal.connect(dispatcher)
            yield
        finally:
            signal.disconnect(dispatcher)

        if err:
            self.fail(err)
