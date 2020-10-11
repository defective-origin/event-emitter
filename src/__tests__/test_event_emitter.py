from unittest import TestCase, main
from unittest.mock import Mock
import asyncio
from ..event_emitter import EventEmitter


class TestEventEmitter(TestCase):

    @classmethod
    def setUp(cls):
        cls.eventEmitter = EventEmitter()

    def test_contains(self):
        with self.subTest('should return True if contains event'):
            self.eventEmitter.on('TEST', lambda: None)

            self.assertTrue(self.eventEmitter.contains('TEST'))

    def test__parse_names(self):
        with self.subTest('should return array of names'):
            result = self.eventEmitter._EventEmitter__parse_names('  a b c  d  ')

            self.assertTrue(result == ['a', 'b', 'c', 'd'])

    def test_enable(self):
        with self.subTest('should enable events'):
            self.eventEmitter.on('TEST_EVENT_1', lambda: None)
            self.eventEmitter.on('TEST_EVENT_2', lambda: None)
            self.eventEmitter.enable('TEST_EVENT_1 TEST_EVENT_2')

            self.assertTrue(self.eventEmitter.is_enabled('TEST_EVENT_1'))
            self.assertTrue(self.eventEmitter.is_enabled('TEST_EVENT_2'))

    def test_disable(self):
        with self.subTest('should disable events'):
            self.eventEmitter.on('TEST_EVENT_1', lambda: None)
            self.eventEmitter.on('TEST_EVENT_2', lambda: None)
            self.eventEmitter.disable('TEST_EVENT_1 TEST_EVENT_2')

            self.assertTrue(self.eventEmitter.is_disabled('TEST_EVENT_1'))
            self.assertTrue(self.eventEmitter.is_disabled('TEST_EVENT_2'))

    def test_empty(self):
        with self.subTest('should enable events'):
            self.eventEmitter.on('TEST_EVENT_1', lambda: None)
            self.eventEmitter.on('TEST_EVENT_2', lambda: None)
            self.eventEmitter.empty()

            self.assertTrue(len(self.eventEmitter._EventEmitter__events) == 0)

    def test_emit(self):
        with self.subTest('should call events'):
            mock_callback1 = Mock()
            mock_callback2 = Mock()

            self.eventEmitter.on('TEST_EVENT_1', mock_callback1)
            self.eventEmitter.on('TEST_EVENT_2', mock_callback2)
            asyncio.run(self.eventEmitter.emit('TEST_EVENT_1 TEST_EVENT_2'))

            self.assertTrue(mock_callback1.called == 1)
            self.assertTrue(mock_callback2.called == 1)

if __name__ == '__main__':
    main()
