from unittest import TestCase, main
from unittest.mock import Mock
import asyncio
from ..event import Event


class TestEvent(TestCase):

    def setUp(self):
        self.event = Event()

    def test_enable(self):
        with self.subTest('should set Event as enabled'):
            self.event.enable()

            self.assertTrue(self.event.is_enabled)

    def test_disable(self):
        with self.subTest('should set Event as disabled'):
            self.event.disable()

            self.assertTrue(self.event.is_disabled)

    def test_on(self):
        with self.subTest('should set unlimited action'):
            mock_callback = lambda: None

            self.event.on(mock_callback)

            self.assertTrue(self.event._Event__actions.popitem()[1].is_unlimited)

    def test_once(self):
        with self.subTest('should set action'):
            mock_callback = lambda: None

            self.event.once(mock_callback, 1)

            self.assertTrue(self.event._Event__actions.popitem()[1].is_limited)

    def test_off(self):
        with self.subTest('should remove action'):
            mock_callback = lambda: None

            self.event.on(mock_callback)
            self.event.off(mock_callback)

            self.assertTrue(len(self.event._Event__actions) == 0)

    def test_emit(self):
        with self.subTest('should call callback if event is enabled'):
            mock_callback = Mock()

            self.event.on(mock_callback)
            asyncio.run(self.event.emit())

            self.assertTrue(mock_callback.called == 1)

        with self.subTest('should not call callback if event is disabled'):
            mock_callback = Mock()

            self.event.on(mock_callback)
            self.event.disable()
            asyncio.run(self.event.emit())

            self.assertTrue(mock_callback.called == 0)

        with self.subTest('should remove all not usable (expired) actions'):
            mock_callback1 = lambda: None
            mock_callback2 = lambda: None

            self.event.once(mock_callback1, 1)
            self.event.once(mock_callback2, 2)
            asyncio.run(self.event.emit())

            self.assertTrue(len(self.event._Event__actions) == 1)
            
if __name__ == '__main__':
    main()
