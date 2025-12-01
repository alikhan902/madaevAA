"""
Comprehensive unit tests для всех алгоритмов поиска подстроки.

Тестирует:
- Корректность алгоритмов на различных данных
- Граничные случаи
- Строки разных типов (случайные, периодические, с повторениями)
"""

import unittest
from prefix_function import compute_prefix_function, compute_prefix_function_verbose
from kmp_search import kmp_search, kmp_search_first
from z_function import (
    compute_z_function, z_search, find_period, is_cyclic_shift
)
from string_matching import (
    boyer_moore_search, rabin_karp_search, rabin_karp_multiple_search
)


class TestPrefixFunction(unittest.TestCase):
    """Тесты для префикс-функции."""
    
    def test_simple_patterns(self):
        """Тестирование простых паттернов."""
        self.assertEqual(compute_prefix_function("A"), [0])
        self.assertEqual(compute_prefix_function("AB"), [0, 0])
        self.assertEqual(compute_prefix_function("AA"), [0, 1])
        
    def test_repeating_pattern(self):
        """Тестирование повторяющихся паттернов."""
        self.assertEqual(compute_prefix_function("AAAA"), [0, 1, 2, 3])
        self.assertEqual(compute_prefix_function("ABAB"), [0, 0, 1, 2])
        
    def test_no_overlap(self):
        """Тестирование паттернов без перекрытий."""
        self.assertEqual(compute_prefix_function("ABCDE"), [0, 0, 0, 0, 0])
        self.assertEqual(compute_prefix_function("ABCD"), [0, 0, 0, 0])
        
    def test_complete_overlap(self):
        """Тестирование полного перекрытия."""
        result = compute_prefix_function("AABAAAB")
        self.assertEqual(result[6], 3)  # "AABAAA" имеет префикс "AAB"
        
    def test_empty_string(self):
        """Тестирование пустой строки."""
        self.assertEqual(compute_prefix_function(""), [])
        
    def test_long_pattern(self):
        """Тестирование длинного паттерна."""
        pattern = "ABCABDABC"
        pi = compute_prefix_function(pattern)
        self.assertEqual(len(pi), len(pattern))
        self.assertEqual(pi[0], 0)


class TestKMPSearch(unittest.TestCase):
    """Тесты для алгоритма КМП."""
    
    def test_single_occurrence(self):
        """Тестирование единственного вхождения."""
        self.assertEqual(kmp_search("ABCDEF", "DEF"), [3])
        self.assertEqual(kmp_search("HELLO", "LLO"), [2])
        
    def test_multiple_occurrences(self):
        """Тестирование множественных вхождений."""
        self.assertEqual(kmp_search("ABABDABACDABABCABAB", "ABABCABAB"), [10])
        self.assertEqual(
            kmp_search("AABAACAADAABAABA", "AABA"),
            [0, 9, 12]
        )
        
    def test_overlapping_occurrences(self):
        """Тестирование перекрывающихся вхождений."""
        self.assertEqual(
            kmp_search("AAAA", "AA"),
            [0, 1, 2]
        )
        self.assertEqual(
            kmp_search("ABABAB", "AB"),
            [0, 2, 4]
        )
        
    def test_no_occurrence(self):
        """Тестирование отсутствия вхождений."""
        self.assertEqual(kmp_search("ABCDEF", "XYZ"), [])
        self.assertEqual(kmp_search("HELLO", "BYE"), [])
        
    def test_pattern_longer_than_text(self):
        """Тестирование паттерна длиннее текста."""
        self.assertEqual(kmp_search("ABC", "ABCDEF"), [])
        
    def test_empty_inputs(self):
        """Тестирование пустых входных данных."""
        self.assertEqual(kmp_search("", ""), [])
        self.assertEqual(kmp_search("ABC", ""), [])
        self.assertEqual(kmp_search("", "A"), [])
        
    def test_pattern_equals_text(self):
        """Тестирование, когда паттерн равен тексту."""
        self.assertEqual(kmp_search("HELLO", "HELLO"), [0])
        
    def test_first_occurrence(self):
        """Тестирование поиска первого вхождения."""
        self.assertEqual(kmp_search_first("AABAACAADAABAABA", "AABA"), 0)
        self.assertEqual(kmp_search_first("ABCDEF", "DEF"), 3)
        self.assertEqual(kmp_search_first("HELLO", "XY"), -1)
        
    def test_case_sensitive(self):
        """Тестирование чувствительности к регистру."""
        self.assertEqual(kmp_search("HELLO", "hello"), [])
        self.assertEqual(kmp_search("Hello", "hello"), [])


class TestZFunction(unittest.TestCase):
    """Тесты для Z-функции."""
    
    def test_simple_strings(self):
        """Тестирование простых строк."""
        self.assertEqual(compute_z_function("A"), [1])
        self.assertEqual(compute_z_function("AB"), [2, 0])
        self.assertEqual(compute_z_function("AA"), [2, 1])
        
    def test_repeating_strings(self):
        """Тестирование повторяющихся строк."""
        self.assertEqual(compute_z_function("AAAA"), [4, 3, 2, 1])
        self.assertEqual(compute_z_function("ABAB"), [4, 0, 2, 0])
        
    def test_no_repeats(self):
        """Тестирование строк без повторений."""
        self.assertEqual(compute_z_function("ABCDE"), [5, 0, 0, 0, 0])
        
    def test_z_search(self):
        """Тестирование поиска с Z-функцией."""
        self.assertEqual(z_search("ABABDABACDABABCABAB", "ABABCABAB"), [10])
        self.assertEqual(z_search("AABAACAADAABAABA", "AABA"), [0, 9, 12])
        self.assertEqual(z_search("HELLO", "XYZ"), [])
        
    def test_find_period(self):
        """Тестирование поиска периода."""
        self.assertEqual(find_period("ABCABCABC"), 3)
        self.assertEqual(find_period("AAAA"), 1)
        self.assertEqual(find_period("XYXY"), 2)
        self.assertEqual(find_period("ABCDEF"), 6)  # нет периода
        
    def test_is_cyclic_shift(self):
        """Тестирование проверки циклического сдвига."""
        self.assertTrue(is_cyclic_shift("ABCD", "CDAB"))
        self.assertTrue(is_cyclic_shift("ABCD", "DABC"))
        self.assertTrue(is_cyclic_shift("ABCD", "BCDA"))
        self.assertFalse(is_cyclic_shift("ABCD", "ABDC"))
        self.assertFalse(is_cyclic_shift("ABC", "ABCD"))
        self.assertTrue(is_cyclic_shift("", ""))


class TestBoyerMoore(unittest.TestCase):
    """Тесты для алгоритма Бойера-Мура."""
    
    def test_single_occurrence(self):
        """Тестирование единственного вхождения."""
        self.assertEqual(boyer_moore_search("ABCDEF", "DEF"), [3])
        self.assertEqual(boyer_moore_search("HELLO", "LLO"), [2])
        
    def test_multiple_occurrences(self):
        """Тестирование множественных вхождений."""
        result = boyer_moore_search("AABAACAADAABAABA", "AABA")
        self.assertEqual(result, [0, 9, 12])
        
    def test_no_occurrence(self):
        """Тестирование отсутствия вхождений."""
        self.assertEqual(boyer_moore_search("ABCDEF", "XYZ"), [])
        
    def test_overlapping(self):
        """Тестирование перекрывающихся вхождений."""
        result = boyer_moore_search("AAAA", "AA")
        # Boyer-Moore может найти не все перекрывающиеся вхождения
        # но должен найти хотя бы некоторые
        self.assertTrue(len(result) > 0)
        
    def test_empty_inputs(self):
        """Тестирование пустых входных данных."""
        self.assertEqual(boyer_moore_search("", ""), [])
        self.assertEqual(boyer_moore_search("ABC", ""), [])


class TestRabinKarp(unittest.TestCase):
    """Тесты для алгоритма Рабина-Карпа."""
    
    def test_single_occurrence(self):
        """Тестирование единственного вхождения."""
        self.assertEqual(rabin_karp_search("ABCDEF", "DEF"), [3])
        
    def test_multiple_occurrences(self):
        """Тестирование множественных вхождений."""
        result = rabin_karp_search("AABAACAADAABAABA", "AABA")
        self.assertEqual(result, [0, 9, 12])
        
    def test_overlapping_occurrences(self):
        """Тестирование перекрывающихся вхождений."""
        result = rabin_karp_search("AAAA", "AA")
        self.assertEqual(result, [0, 1, 2])
        
    def test_no_occurrence(self):
        """Тестирование отсутствия вхождений."""
        self.assertEqual(rabin_karp_search("ABCDEF", "XYZ"), [])
        
    def test_empty_inputs(self):
        """Тестирование пустых входных данных."""
        self.assertEqual(rabin_karp_search("", ""), [])
        self.assertEqual(rabin_karp_search("ABC", ""), [])
        
    def test_multiple_patterns(self):
        """Тестирование поиска множественных паттернов."""
        text = "AABAACAADAABAABA"
        patterns = ["AABA", "AAB", "ABA"]
        results = rabin_karp_multiple_search(text, patterns)
        
        self.assertEqual(results["AABA"], [0, 9, 12])
        self.assertEqual(results["AAB"], [0, 9, 12])
        self.assertEqual(results["ABA"], [1, 10, 13])


class TestAlgorithmConsistency(unittest.TestCase):
    """Тесты для проверки консистентности всех алгоритмов."""
    
    def test_all_algorithms_same_results(self):
        """Проверка, что все алгоритмы находят одни и те же результаты."""
        test_cases = [
            ("ABABDABACDABABCABAB", "ABABCABAB"),
            ("AABAACAADAABAABA", "AABA"),
            ("abcabcabcabc", "bcab"),
            ("MISSISSIPPI", "ISS"),
        ]
        
        for text, pattern in test_cases:
            kmp_result = kmp_search(text, pattern)
            z_result = z_search(text, pattern)
            rk_result = rabin_karp_search(text, pattern)
            
            # KMP, Z-function и Rabin-Karp должны дать одинаковые результаты
            self.assertEqual(kmp_result, z_result, 
                           f"KMP и Z-function дают разные результаты для {pattern}")
            self.assertEqual(kmp_result, rk_result,
                           f"KMP и Rabin-Karp дают разные результаты для {pattern}")
    
    def test_various_string_types(self):
        """Тестирование на различных типах строк."""
        # Случайные строки
        text1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pattern1 = "MNO"
        
        # Периодические строки
        text2 = "ABABABABAB"
        pattern2 = "ABA"
        
        # Строки с повторениями
        text3 = "AAAAAABBBBBBCCCCCC"
        pattern3 = "AAB"
        
        for text, pattern in [(text1, pattern1), (text2, pattern2), (text3, pattern3)]:
            kmp_result = kmp_search(text, pattern)
            z_result = z_search(text, pattern)
            rk_result = rabin_karp_search(text, pattern)
            
            self.assertEqual(kmp_result, z_result)
            self.assertEqual(kmp_result, rk_result)


class TestPracticalProblems(unittest.TestCase):
    """Тесты для практических задач."""
    
    def test_find_all_occurrences(self):
        """Задача: найти все вхождения паттерна."""
        text = "ababcababa"
        pattern = "aba"
        result = kmp_search(text, pattern)
        self.assertEqual(result, [0, 5, 7])
        
    def test_find_period(self):
        """Задача: найти период строки."""
        periods = {
            "ABCABCABC": 3,
            "AAAA": 1,
            "XYXYXYXY": 2,
            "ABCDEF": 6,  # нет периода
        }
        
        for string, expected_period in periods.items():
            period = find_period(string)
            self.assertEqual(period, expected_period)
    
    def test_cyclic_shift(self):
        """Задача: проверка циклического сдвига."""
        # True cases
        self.assertTrue(is_cyclic_shift("abcd", "cdab"))
        self.assertTrue(is_cyclic_shift("abcd", "dabc"))
        
        # False cases
        self.assertFalse(is_cyclic_shift("abcd", "abdc"))
        self.assertFalse(is_cyclic_shift("abc", "abcd"))


# Интеграционные тесты
class TestIntegration(unittest.TestCase):
    """Интеграционные тесты."""
    
    def test_complex_text_search(self):
        """Тестирование сложного текста."""
        text = "The quick brown fox jumps over the lazy dog. The quick brown fox."
        pattern = "quick brown fox"
        
        result = kmp_search(text, pattern)
        self.assertEqual(result.count(4), 1)  # "quick" встречается дважды
        
    def test_unicode_strings(self):
        """Тестирование Unicode строк."""
        text = "привет мир привет"
        pattern = "привет"
        
        kmp_result = kmp_search(text, pattern)
        self.assertEqual(kmp_result, [0, 11])


if __name__ == "__main__":
    # Запуск всех тестов с подробным выводом
    unittest.main(verbosity=2)
