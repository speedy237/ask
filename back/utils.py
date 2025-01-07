from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.client import HTTPException
from smtplib import SMTP
import smtplib
from typing import List
from requestData import ApplicationData, Candidate
from database import getData
from sqlalchemy import create_engine # type: ignore
from collections import defaultdict


EMAIL_CONFIG = {
    "smtp_server": "smtp.mail.yahoo.com",
    "smtp_port": 587,
    "username": "yiyuemej@yahoo.fr",
    "password": "vkpknbjvbyjphgbj",
}

def create_custom_xml_from_any_data(data, output_file):
    """
    Convertit n'importe quel tableau de dictionnaires en format XML avec des balises <label> et <value>.
    
    :param data: Liste de dictionnaires avec des paires clé-valeur
    :param output_file: Chemin du fichier XML à créer
    """
    # Créer la racine XML
    root = ET.Element("data")

    for record in data:
        entry = ET.SubElement(root, "entry")

        for key, value in record.items():
            label = ET.SubElement(entry, "label")
            label.text = str(key)

            val = ET.SubElement(entry, "value")
            val.text = str(value)

    # Convertir l'arbre XML en chaîne et l'écrire dans un fichier
    tree = ET.ElementTree(root)
    with open(output_file, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)


def send_email_with_gmail(recipient_email: str, candidates: List[ApplicationData]):
    try:
        # Création du contenu de l'email
        subject = "Top Candidates for the Selected Role"
        body = """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
        """
        body+=f"""
        Bonjour, <br/>
        
            <h1>Top  Candidates </h1>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Experience</th>
                        <th>Certifications</th>
                        <th>Diplome</th>
                        <th>Soft Skills</th>
                        <th>Hard Skills</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Ajout des lignes des candidats au tableau
        for candidate in candidates:
            body += f"""
                    <tr>
                        <td>{candidate.applicantName}</td>
                        <td>{candidate.Score}</td>
                        <td>{candidate.Experience}</td>
                        <td>{candidate.Certification}</td>
                        <td>{candidate.Diplome}</td>
                        <td>{candidate.Soft}</td>
                        <td>{candidate.Hard}</td>
                    </tr>
            """

        body += """
                </tbody>
            </table>
        </body>
        </html>
        """

        # Configuration du message
        msg = MIMEMultipart()
        msg['From'] = "yiyuemej@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('yiyuemej@yahoo.fr', 'vkpknbjvbyjphgbj')
        server.sendmail('yiyuemej@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
    
def send_email(recipient_email: str, applications: List[ApplicationData]):
    try:
        # Organiser les candidats par IDJob
        grouped_candidates = defaultdict(list)
        for application in applications:
            grouped_candidates[application.IDjob].append(application)

        # Création du contenu de l'email
        subject = "Top Candidates for the Selected Roles"
        body = """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
        Bonjour, <br/>
        """

        # Génération des tableaux pour chaque IDJob
        for IDJob, candidates in grouped_candidates.items():
            role = candidates[0].Role  # Supposons que le rôle est identique pour un IDJob donné
            body += f"<h2>Top Candidates for {role}</h2>"
            body += """
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Experience</th>
                        <th>Certifications</th>
                        <th>Diplome</th>
                        <th>Soft Skills</th>
                        <th>Hard Skills</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for candidate in candidates:
                body += f"""
                    <tr>
                        <td>{candidate.applicantName}</td>
                        <td>{candidate.Score}</td>
                        <td>{candidate.Experience}</td>
                        <td>{candidate.Certification}</td>
                        <td>{candidate.Diplome}</td>
                        <td>{candidate.Soft}</td>
                        <td>{candidate.Hard}</td>
                    </tr>
                """

            body += """
                </tbody>
            </table>
            <br/>
            """

        body += """
        </body>
        </html>
        """

        # Configuration du message
        msg = MIMEMultipart()
        msg['From'] = "yiyuemej@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('yiyuemej@yahoo.fr', 'vkpknbjvbyjphgbj')
        server.sendmail('yiyuemej@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

def send_email2(recipient_email: str, applications: List[ApplicationData], topN: int):
    try:
        # Organiser les candidats par IDJob
        grouped_candidates = defaultdict(list)
        for application in applications:
            grouped_candidates[application.IDjob].append(application)

        # Création du contenu de l'email
        subject = f"Top {topN} Candidates for Each Roles"
        body = """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
        """
        body+=f"""
        Bonjour, <br/>
        Veuilez trouver ci-dessous le top {topN} des candidats pour chaque poste
        """

        # Génération des tableaux pour chaque IDJob
        for IDjob, candidates in grouped_candidates.items():
            role = candidates[0].Role  # Supposons que le rôle est identique pour un IDJob donné
            body += f"<h2> {role} </h2>"
            body += """
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Experience</th>
                        <th>Date</th>
                        
                    </tr>
                </thead>
                <tbody>
            """

            # Prendre uniquement les topN candidats
            top_candidates = candidates[:topN]

            for candidate in top_candidates:
                body += f"""
                    <tr>
                        <td>{candidate.applicantName}</td>
                        <td>{candidate.Score}</td>
                        <td>{candidate.Experience}</td>
                        <td>{candidate.Date}</td>
                      
                    </tr>
                """

            body += """
                </tbody>
            </table>
            <br/>


            
            """

        body += """
        Cordialement,
        L'Equipe Aubay
        </body>
        </html>
        """

        # Configuration du message
        msg = MIMEMultipart()
        msg['From'] = "gaelkamdem@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('gaelkamdem@yahoo.fr', 'nzszqfqetawnqkch')
        server.sendmail('gaelkamdem@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

def send_email3(recipient_email: str, applications: List[ApplicationData], topN: int):
    try:
        # Organiser les candidats par IDJob
        grouped_candidates = defaultdict(list)
        for application in applications:
            grouped_candidates[application.IDjob].append(application)

        # Création du contenu de l'email
        subject = f"Top {topN} Candidates for Each Roles"
        body = """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
                .low-score {
                    background: linear-gradient(to right, red, white);
                }
                .high-score {
                    background: linear-gradient(to right, green, white);
                }
            </style>
        </head>
        <body>
        Bonjour, <br/>
        """

        # Génération des tableaux pour chaque IDJob
        for IDjob, candidates in grouped_candidates.items():
            role = candidates[0].Role  # Supposons que le rôle est identique pour un IDJob donné
            body += f"<h2>Top {topN} Candidates for {role}</h2>"
            body += """
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Experience</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
            """

            # Prendre uniquement les topN candidats
            top_candidates = candidates[:topN]

            for candidate in top_candidates:
                score_class = "low-score" if candidate.Score < 50 else "high-score"
                body += f"""
                    <tr>
                        <td>{candidate.applicantName}</td>
                        <td class=\"{score_class}\">{candidate.Score}</td>
                        <td>{candidate.Experience}</td>
                        <td>{candidate.Date}</td>
                    </tr>
                """

            body += """
                </tbody>
            </table>
            <br/>
            """

        body += """
        </body>
        </html>
        """

        # Configuration du message
        msg = MIMEMultipart()
        msg['From'] = "yiyuemej@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('yiyuemej@yahoo.fr', 'vkpknbjvbyjphgbj')
        server.sendmail('yiyuemej@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
