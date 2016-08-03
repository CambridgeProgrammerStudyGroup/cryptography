using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace SimpleCaesar
{
	class MainClass
	{
		static Regex rx = new Regex("[a-z]");

		public static void Main(string[] args)
		{
			IEnumerable<char> text = File.ReadAllText("cipher.txt")
				.ToLower()
				.Where(c => rx.IsMatch(c.ToString()));

			var countDictionary = new Dictionary<char,int>();

			foreach (char item in text) {
				if (countDictionary.ContainsKey(item))
					countDictionary[item]++;
				else
					countDictionary[item] = 1;
			}

			foreach (KeyValuePair<char,int> kvp in countDictionary) {
				Console.WriteLine("{0} ({1}): {2}", kvp.Key, (int)kvp.Key, kvp.Value);
			}

			// find the most common letter
			KeyValuePair<char,int> mostCommon = new KeyValuePair<char, int>('?',0);
			foreach (KeyValuePair<char,int> current in countDictionary) {
				if (current.Value > mostCommon.Value)
					mostCommon = current;
			}

			Console.WriteLine("Most common was {0} with {1}", mostCommon.Key, mostCommon.Value);

			// work out the shift
			int shift = mostCommon.Key - 101;
			Console.WriteLine("The shift was: {0}", shift);

			// reverse the encryption
			var result = File.ReadAllText("cipher.txt").Select(c => decrypt(c, shift)).ToArray();

			Console.WriteLine(new String(result));
		}

		private static char decrypt(char c, int shift) {
			if (rx.IsMatch(c.ToString())) {
				var result = (char)(c - shift);
				if (result < 97)
					result = (char)(result + 26);
				return result;
			} else
				return c;
		}
	}
}
