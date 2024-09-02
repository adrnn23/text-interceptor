import tkinter as tk
from tkinter import messagebox
import re
import spacy

class InformationExtractor:
    def __init__(self):
        self.nlp_pl = spacy.load("pl_core_news_sm")
        self.nlp_en = spacy.load("en_core_web_sm")

    def findPhoneNumbers(self, text):
        pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{3,4}\b'
        numbers = re.findall(pattern, text)
        numbers = [n for n in numbers if not re.match(r'\b\d{1,2}[-/.\s]\d{1,2}[-/.\s]\d{2,4}\b', n)]
        return numbers

    def findDates(self, text):
        pattern = r'\b(?:\d{1,2}[-/.\s]\d{1,2}[-/.\s]\d{2,4}|\d{4}[-/.\s]\d{1,2}[-/.\s]\d{1,2})\b'
        dates = re.findall(pattern, text)
        return dates
    
    def findNamedEntitiesPL(self, text):
        return self.findNamedEntities(text, self.nlp_pl)

    def findNamedEntitiesEN(self, text):
        return self.findNamedEntities(text, self.nlp_en)

    def findNamedEntities(self, text, nlp_model):
        doc = nlp_model(text)
        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        return persons

    def displayResults(self, numbers, dates, persons):
        result = ""

        if numbers:
            result += "Found phone numbers:\n" + "\n".join(numbers) + "\n\n"
        else:
            result += "No phone numbers found.\n\n"

        if dates:
            result += "Found dates:\n" + "\n".join(dates) + "\n\n"
        else:
            result += "No dates found.\n\n"

        if persons:
            result += "Found names:\n" + "\n".join(persons) + "\n\n"
        else:
            result += "No names found.\n\n"

        messagebox.showinfo("Search Results", result)


    def getInformation(self, filepath):
        try:
            with open(filepath, 'r') as file:
                text = file.read()
            numbers = self.findPhoneNumbers(text)
            dates = self.findDates(text)
            personsPl = self.findNamedEntitiesPL(text)
            personsEn = self.findNamedEntitiesEN(text)
            persons = list(set(personsPl))+list(set(personsEn))
            self.displayResults(numbers, dates, persons)

        except Exception as e:
            messagebox.showerror("Error", str(e))