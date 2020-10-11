from unittest import TestCase, main
from unittest.mock import Mock
import asyncio
from ..event_emitter import EventEmitter


class TestEventEmitter(TestCase):
    def test_contains(self):
        with self.subTest('should return True if contains event'):
            eventEmitter = EventEmitter()

            eventEmitter.on('TEST', lambda: None)

            self.assertTrue(eventEmitter.contains('TEST'))

    def test__parse_names(self):
        with self.subTest('should return array of names'):
            eventEmitter = EventEmitter()

            result = eventEmitter._EventEmitter__parse_names('  a b c  d  ')

            self.assertTrue(result == ['a', 'b', 'c', 'd'])

    def test_enable(self):
        with self.subTest('should enable events'):
            eventEmitter = EventEmitter()

            eventEmitter.on('TEST_EVENT_1', lambda: None)
            eventEmitter.on('TEST_EVENT_2', lambda: None)
            eventEmitter.enable('TEST_EVENT_1 TEST_EVENT_2')

            self.assertTrue(eventEmitter.is_enabled('TEST_EVENT_1'))
            self.assertTrue(eventEmitter.is_enabled('TEST_EVENT_2'))

    def test_disable(self):
        with self.subTest('should disable events'):
            eventEmitter = EventEmitter()

            eventEmitter.on('TEST_EVENT_1', lambda: None)
            eventEmitter.on('TEST_EVENT_2', lambda: None)
            eventEmitter.disable('TEST_EVENT_1 TEST_EVENT_2')

            self.assertTrue(eventEmitter.is_disabled('TEST_EVENT_1'))
            self.assertTrue(eventEmitter.is_disabled('TEST_EVENT_2'))

    def test_empty(self):
        with self.subTest('should enable events'):
            eventEmitter = EventEmitter()

            eventEmitter.on('TEST_EVENT_1', lambda: None)
            eventEmitter.on('TEST_EVENT_2', lambda: None)
            eventEmitter.empty()

            self.assertTrue(len(eventEmitter._EventEmitter__events) == 0)

    def test_emit(self):
        with self.subTest('should call events'):
            eventEmitter = EventEmitter()
            mock_callback1 = Mock()
            mock_callback2 = Mock()

            eventEmitter.on('TEST_EVENT_1', mock_callback1)
            eventEmitter.on('TEST_EVENT_2', mock_callback2)
            asyncio.run(eventEmitter.emit('TEST_EVENT_1 TEST_EVENT_2'))

            self.assertTrue(mock_callback1.called == 1)
            self.assertTrue(mock_callback2.called == 1)

if __name__ == '__main__':
    main()
