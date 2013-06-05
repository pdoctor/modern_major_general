import unittest
import os.path
import shutil
from modern_major_general import MMG
import itertools

class TestModernMajorGeneral(unittest.TestCase):

	basepath = os.path.dirname(__file__)
	test_directory = os.path.join(basepath, "test_data")
	test_sub_directory = os.path.join(test_directory, "test_sub_data")
	test_file_name = os.path.join(test_directory, "test_file_one.txt")

	def setUp(self):
		
		self.make_directory(self.test_directory)
		self.make_test_file(self.test_file_name, self.file_one_content)

		self.make_directory(self.test_sub_directory)
		self.make_test_file(os.path.join(self.test_sub_directory, "test_file_two.txt"), self.file_two_content)

		self.test_mmg = MMG(find_pattern="grippe being", in_directory=".")

	def tearDown(self):
		shutil.rmtree(self.test_directory)

	def file_one_content(self):
		yield """CHAPTER I

"Well, Prince, so Genoa and Lucca are now just family estates of the
Buonapartes. But I warn you, if you don't tell me that this means war,
if you still try to defend the infamies and horrors perpetrated by that
Antichrist--I really believe he is Antichrist--I will have nothing more
to do with you and you are no longer my friend, no longer my 'faithful
slave,' as you call yourself! But how do you do? I see I have frightened
you--sit down and tell me all the news."

It was in July, 1805, and the speaker was the well-known Anna Pavlovna
Scherer, maid of honor and favorite of the Empress Marya Fedorovna. With
these words she greeted Prince Vasili Kuragin, a man of high rank and
importance, who was the first to arrive at her reception. Anna Pavlovna
had had a cough for some days. She was, as she said, suffering from la
grippe; grippe being then a new word in St. Petersburg, used only by the
elite."""

	def file_two_content(self):
		yield """All her invitations without exception, written in French, and delivered
by a scarlet-liveried footman that morning, ran as follows:

"If you have nothing better to do, Count (or Prince), and if the
prospect of spending an evening with a poor invalid is not too terrible,
I shall be very charmed to see you tonight between 7 and 10--Annette
Scherer."

"Heavens! what a virulent attack!" replied the prince, not in the least
disconcerted by this reception. He had just entered, wearing an
embroidered court uniform, knee breeches, and shoes, and had stars on
his breast and a serene expression on his flat face. He spoke in that
refined French in which our grandfathers not only spoke but thought, and
with the gentle, patronizing intonation natural to a man of importance
who had grown old in society and at court. He went up to Anna Pavlovna,
kissed her hand, presenting to her his bald, scented, and shining head,
and complacently seated himself on the sofa."""

	def make_directory(self, directory_name):
		if not os.path.exists(directory_name):
			os.makedirs(directory_name)

	def make_test_file(self, test_file_name, test_content_generator):
		with open(test_file_name, 'w') as file_handle:
			for line in test_content_generator():
				file_handle.write(line)
				file_handle.write("\n")

	def test_match_pattern_finds_in_text(self):
		line_matcher = self.test_mmg._build_match_pattern("test text")
		self.assertTrue(line_matcher("test test text extra"))

	def test_match_pattern_finds_exact_match_text(self):
		line_matcher = self.test_mmg._build_match_pattern("test text")
		self.assertTrue(line_matcher("test text"))


	def test_match_pattern_does_not_find_text(self):
		line_matcher = self.test_mmg._build_match_pattern("grippe being")
		self.assertFalse(line_matcher("test test text extra"))

	def test_match_pattern_in_base_dir_file(self):
		line_matcher = self.test_mmg._build_match_pattern("grippe being")
		found = reduce(lambda x, y: x or y, itertools.imap(line_matcher, self.test_mmg._read_files_in_directory(self.test_directory)))

		self.assertTrue(found)

	def test_match_pattern_in_sub_dir_file(self):
		line_matcher = self.test_mmg._build_match_pattern("scarlet-liveried footman")
		found = reduce(lambda x, y: x or y, itertools.imap(line_matcher, self.test_mmg._read_files_in_directory(self.test_directory)))

		self.assertTrue(found)

	def test_no_pattern_in_sub_dir_file(self):
		line_matcher = self.test_mmg._build_match_pattern("explosive flatulence")
		found = reduce(lambda x, y: x or y, itertools.imap(line_matcher, self.test_mmg._read_files_in_directory(self.test_directory)))

		self.assertFalse(found)

	def test_get_input_source_returns_iterable_for_file(self):
		try:
			test_dict = { "in_file" : self.test_file_name }
			iter_object = self.test_mmg._get_input_source(test_dict)
			it = iter(iter_object)
			self.assertTrue(True)
		except TypeError: 
			self.assertTrue(False)

	def test_get_input_source_returns_iterable_for_file(self):
		try:
			test_dict = { "in_directory" : self.test_directory }
			iter_object = self.test_mmg._get_input_source(test_dict)
			it = iter(iter_object)
			self.assertTrue(True)
		except TypeError: 
			self.assertTrue(False)

	def test_get_input_source_raises_both_file_and_dir(self):
		test_dict = { "in_directory" : self.test_directory, "in_file" : self.test_file_name }
		with self.assertRaises(ValueError):
			self.test_mmg._get_input_source(test_dict)

	def test_get_input_source_raises_neither_file_nor_dir(self):
		test_dict = { }
		with self.assertRaises(ValueError):
			self.test_mmg._get_input_source(test_dict)

	def test_get_input_source_raises_file_does_not_exist(self):
		test_dict = { "in_file" : "not_a_real_file.txt" }
		with self.assertRaises(IOError):
			self.test_mmg._get_input_source(test_dict)

	def test_get_input_source_raises_directory_does_not_exist(self):
		test_dict = { "in_directory" : "not_a_real_dir" }
		with self.assertRaises(IOError):
			self.test_mmg._get_input_source(test_dict)

	def test_print_matches_to_screen(self):
		self.test_mmg.print_matches_to_screen()


if __name__ == '__main__':
    unittest.main()