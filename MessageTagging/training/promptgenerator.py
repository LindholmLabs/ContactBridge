import csv
import random


class PromptGenerator:
    def __init__(self, companies_file, names_file):
        self.companies = self.load_companies(companies_file)
        self.names = self.load_names(names_file)

    def load_companies(self, file_path):
        companies = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                companies.append(row[1])  # Assumes companies are in the second column
        return companies

    def load_names(self, file_path):
        names = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                names.append(row[3])  # Assumes names are in the third column
        return names

    def generate_prompt(self):
        tones_en = [
            "formal", "informal", "friendly", "professional", "courteous",
            "casual", "polite", "respectful", "relaxed", "enthusiastic",
            "serious", "light-hearted", "supportive", "constructive"
        ]
        actions_en = [
            "inquiry", "message", "response", "joboffer", "answer", "proposal",
            "feedback", "update", "announcement", "invitation", "follow-up",
            "clarification", "confirmation", "reminder"
        ]
        verbs_en = [
            "create", "generate", "compose", "craft", "formulate", "devise",
            "construct", "design", "develop", "draft", "prepare", "produce",
            "assemble", "originate"
        ]

        tones_sv = [
            "formellt", "informellt", "vänlig", "professionell", "artigt",
            "avslappnat", "hövlig", "respektfull", "avslappnad", "entusiastisk",
            "allvarlig", "lättsinnigt", "stödjande", "konstruktiv"
        ]
        actions_sv = [
            "förfrågan", "meddelande", "svar", "jobberbjudande", "svar", "förslag",
            "återkoppling", "uppdatering", "meddelande", "inbjudan", "uppföljning",
            "förtydligande", "bekräftelse", "påminnelse"
        ]
        verbs_sv = [
            "skapa", "generera", "komponera", "utforma", "formulera", "utveckla",
            "konstruera", "designa", "utveckla", "utkasta", "förbereda", "producera",
            "sammanställ", "originera"
        ]

        company = random.choice(self.companies)
        name = random.choice(self.names)

        language = random.choice(["en", "sv"])
        if language == "en":
            tone = random.choice(tones_en)
            action = random.choice(actions_en)
            verb = random.choice(verbs_en)
            prompt = f"{verb} {tone} {action} from {company} to {name}"
        else:
            tone = random.choice(tones_sv)
            action = random.choice(actions_sv)
            verb = random.choice(verbs_sv)
            prompt = f"{verb} {tone} {action} från {company} till {name}"

        return prompt


# Usage:
if __name__ == "__main__":
    prompt_generator = PromptGenerator('companies.csv', 'names.csv')
    print(prompt_generator.generate_prompt())