import os
import unittest
from argparse import Namespace

from src.hasher.hasher import do_encrypt, do_decrypt, main
from tests.base.base_test import BaseFileSystemTest
from tests.base.structures import File


class TestRunEncryptor(BaseFileSystemTest, unittest.TestCase):
    test_folder = "./tmp/test_folder"
    program_content = '''
        // testing hello world programme
        #include <stdio.h>
        int main() {
            printf("Hello World!");
            return 0;
        } 
    '''
    files = [
        File("program.c", program_content),
    ]

    def __encrypt_and_delete_original(self):
        self.execute_in_test_folder(lambda: do_encrypt('key', 'program.c'))
        self.execute_in_test_folder(lambda: os.remove('program.c'))

    def test_encr_file_generation(self):
        self.setup_test_folder()
        self.execute_in_test_folder(lambda: do_encrypt('key', 'program.c'))
        self.assertEqual(2, len(self.get_test_folder_state().files))
        self.assertEqual(1, len([file for file in self.get_test_folder_state().files if file.name == 'program.c.encr']))
        self.clear_test_folder()

    def test_encr_file_content(self):
        self.setup_test_folder()
        self.execute_in_test_folder(lambda: do_encrypt('key', 'program.c'))
        encr_file = [file for file in self.get_test_folder_state().files if file.name == 'program.c.encr'][0]
        self.assertNotEqual(self.program_content, encr_file.content)
        self.clear_test_folder()

    def test_decription(self):
        self.setup_test_folder()
        self.__encrypt_and_delete_original()
        self.execute_in_test_folder(lambda: do_decrypt('key', 'program.c.encr'))
        self.assertEqual(2, len(self.get_test_folder_state().files))
        self.assertEqual(1, len([file for file in self.get_test_folder_state().files if file.name == 'program.c']))
        self.clear_test_folder()

    def test_decription_content(self):
        self.setup_test_folder()
        self.__encrypt_and_delete_original()
        self.execute_in_test_folder(lambda: do_decrypt('key', 'program.c.encr'))
        decr_file = [file for file in self.get_test_folder_state().files if file.name == 'program.c'][0]
        self.assertEqual(self.program_content, decr_file.content)
        self.clear_test_folder()

    def test_decryption_with_wrong_key(self):
        self.setup_test_folder()
        self.__encrypt_and_delete_original()
        self.execute_in_test_folder(lambda: do_decrypt('wrong_key', 'program.c.encr'))
        self.assertEqual(1, len(self.get_test_folder_state().files))
        self.assertEqual(1, len([file for file in self.get_test_folder_state().files if file.name == 'program.c.encr']))
        self.assertEqual(0, len([file for file in self.get_test_folder_state().files if file.name == 'program.c']))
        self.clear_test_folder()

    def test_flag_mode_encrypt(self):
        self.setup_test_folder()
        self.execute_in_test_folder(
            lambda: main(flag_mode=True, args=Namespace(action='encrypt', key_phrase='key', input_file='program.c')))
        self.assertEqual(2, len(self.get_test_folder_state().files))
        self.assertEqual(1, len([file for file in self.get_test_folder_state().files if file.name == 'program.c.encr']))
        self.clear_test_folder()

    def test_flag_mode_decrypt(self):
        self.setup_test_folder()
        self.__encrypt_and_delete_original()
        self.execute_in_test_folder(
            lambda: main(flag_mode=True, args=Namespace(action='decrypt', key_phrase='key', input_file='program.c.encr')))
        self.assertEqual(2, len(self.get_test_folder_state().files))
        self.assertEqual(1, len([file for file in self.get_test_folder_state().files if file.name == 'program.c']))
        self.clear_test_folder()