from unittest import TestCase
from unittest.mock import patch, Mock
from docupy.markdown import *

class MarkdownToHtmlTests(TestCase):

    @patch("docupy.markdown.text_to_blocks")
    def test_can_convert_markdown_to_html(self, mock_blocks):
        mock_blocks.return_value = ["block1", "block2"]
        markdown = "markdown"
        html = markdown_to_html(markdown)
        mock_blocks.assert_called_with("markdown")
        self.assertEqual(html, "block1\nblock2")



class BlockSplittingTests(TestCase):

    def test_single_line_returns_single_block(self):
        blocks = text_to_blocks("A line.")
        self.assertEqual(blocks, ["A line."])


    def test_one_line_break_not_enough(self):
        blocks = text_to_blocks("A line.\nA second line?")
        self.assertEqual(blocks, ["A line. A second line?"])


    def test_can_break_into_blocks(self):
        blocks = text_to_blocks("A line.\n\nA second line\n\nThird line")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_empty_lines_ignored(self):
        blocks = text_to_blocks("A line.\n\n\n\nA second line\n\n\nThird line\n")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_windows_line_breaks(self):
        blocks = text_to_blocks("A line.\r\n\r\nA second line")
        self.assertEqual(blocks, ["A line.", "A second line"])



class BlockToHtmlTests(TestCase):

    @patch("docupy.markdown.create_special_html")
    def test_can_get_special_html(self, mock_html):
        mock_html.return_value = "<X>...</X>"
        html = block_to_html("!block")
        mock_html.assert_called_with("!block")
        self.assertEqual(html, "<X>...</X>")
        html = block_to_html("#block")
        mock_html.assert_called_with("#block")
        self.assertEqual(html, "<X>...</X>")


    @patch("docupy.markdown.create_paragraph_html")
    def test_can_get_special_html(self, mock_html):
        mock_html.return_value = "<X>...</X>"
        html = block_to_html("block")
        mock_html.assert_called_with("block")
        self.assertEqual(html, "<X>...</X>")



class SpecialHtmlTests(TestCase):

    def test_can_create_heading_html(self):
        html = create_special_html("##     head")
        self.assertEqual(html, "<h2>head</h2>")
        html = create_special_html("########HHH")
        self.assertEqual(html, "<h8>HHH</h8>")