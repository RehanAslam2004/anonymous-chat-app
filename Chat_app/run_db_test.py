from time import sleep
import db
print('Calling get_messages for room 1234')
msgs = db.get_messages('1234')
print('Result type:', type(msgs))
print('Result preview:', msgs[:5] if isinstance(msgs, list) else msgs)
print('\nNow attempting to save a test message...')
res = db.save_message('1234','test_handle','this is a test saved message')
print('Save result:', type(res), res)
