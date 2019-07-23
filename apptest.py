
################# IMPORTATION DES MODULES ########################""
from flask import Flask, render_template,request,redirect, url_for, flash
import psycopg2
app = Flask(__name__)
app.secret_key= "flash message"
#############################CONNECTION A LA BADD POSTGRESQL#######################""
def cire():
        try:
    
                        con = psycopg2.connect(
                        database="projet2",
                        user="cire",
                        password="Ciréric1990&",
                        host="localhost",
                        port="5432"
                        )
                        return con
        except(Exception) as error:
                print("Problèmes de connection au serveur", error)

con = cire()
curseur=con.cursor()
                        

@app.route('/')
def home():
    return render_template('accueil.html')

#Rédirection vers la page accueil
@app.route('/accueil')
def accueil():
    return render_template('accueil.html')


###################INSERTION DANS LA BDD TABLE APPRENANT##################

@app.route('/inscription', methods = ['GET','POST'])
def index():
        curseur.execute("SELECT * FROM promo")
        apprenant=curseur.fetchall()
        if request.method == "POST":
                flash ("Données insérées avec succès")
                matricule = request.form['matricule']
                prenom = request.form['prenom']
                nom = request.form['nom']
                datenaiss = request.form['Date Naiss']
                nom_promo = int(request.form['Nom Promo'])
                cur = con.cursor()
                cur.execute('INSERT INTO apprenant (matricule, prenom, nom, datenaiss,Idpromo,statut) VALUES(%s,%s,%s,%s,%s,%s)', (matricule,prenom,nom,datenaiss,nom_promo, 'inscrit'))
                con.commit()
        return render_template ('inscription.html',  data = apprenant)


###################INSERTION DANS LA BDD TABLE REFERENTIEL##################


@app.route('/referentiel', methods = ['GET','POST'])
def index1():
        if request.method == "POST":
                flash ("Données insérées avec succès")
                nomref = request.form['Nom Referentiel']
                ajout = "INSERT INTO referentiel (nomref) VALUES(%s)"
                curseur.execute(ajout,(nomref,))
                con.commit()
        return render_template ('referentiel.html')


###########################################################################

###################INSERTION DANS LA BDD TABLE PROMOTION ##################


@app.route('/promotion', methods = ['GET','POST'])
def index2():
        curseur.execute("SELECT * FROM referentiel")
        promo=curseur.fetchall()
        if request.method == "POST":
                flash ("Données insérées avec succès")
                nompromo = request.form['nompromo']
                date_debut = request.form['date_debut']
                date_fin = request.form['date_fin']
                nom_ref = int(request.form['referentiel'])
                cur=con.cursor()
                cur.execute("INSERT INTO promo (nompromo,date_debut,date_fin,idref) VALUES(%s,%s,%s,%s)",(nompromo,date_debut,date_fin,nom_ref))
                con.commit()
        return render_template ('promotion.html',  data1 = promo)

#########################################################################################""

##########################################UPDATE APPRENANT##################################

@app.route('/update', methods = ['GET','POST'])
def updateapp():
        cur=con.cursor()
        cur.execute("SELECT * FROM apprenant")
        var1=cur.fetchall()
        con.commit()

        cur.execute("SELECT * FROM promo")
        var2=cur.fetchall()
        con.commit()

        if request.method == 'POST':
                id_data = request.form['id']
                matricule = request.form['matricule']
                prenom = request.form['prenom']
                nom = request.form['nom']
                datenaiss = request.form['datenaiss']
                Idpromo = int(request.form['Nom Promo'])
                cur = con.cursor()
                cur.execute("""
                UPDATE apprenant
                SET matricule=%s, prenom=%s, nom=%s, datenaiss=%s, idpromo=%s
                WHERE idapprenant=%s """, (matricule, prenom, nom,datenaiss,Idpromo,id_data))
                con.commit()
                flash ("Données mises à jour avec succès")

                cur=con.cursor()
                cur.execute("SELECT * FROM apprenant")
                var3=cur.fetchall()
                con.commit()

                return render_template ('update.html', apprenant = var3, promo = var2) 

        return render_template ('update.html', apprenant = var1, promo = var2)

###########################################################################################



#########################UPDATE REFERENTIEL##################################


#######PREMIERE ETAPE: LISTAGE#############

@app.route('/updateref', methods = ['GET','POST'])
def updateref():
        cur=con.cursor()
        cur.execute("SELECT referentiel.nomref, referentiel.idref, promo.idpromo FROM referentiel, promo WHERE referentiel.idref=promo.idref")
        data2=cur.fetchall()
        con.commit()
        
        cur=con.cursor()
        cur.execute("SELECT * FROM promo")
        bac = cur.fetchall()
        con.commit()

        return render_template('updateref.html', promo=data2,referentiel=bac)


#################"#DEUXIEME ETAPE: UPDATE#############

@app.route('/updateref', methods = ['POST','GET'])
def updateref2():
        if request.method == 'POST':
                #id_data = request.form['id_data']
                idref = request.form['idref']
                nomref =request.form['nomref']
                cur = con.cursor()
                cur.execute("""
                UPDATE referentiel
                SET nomref=%s
                WHERE idref=%s """, (idref,nomref))
                con.commit()
                flash ("Données mises à jour avec succès")

        return redirect(url_for('updateref'))


#######################################################################

######UPDATE PROMO###############

                        # PREMIERE ETAPE: ######LISTAGE###########

@app.route('/update1')
def update1():
        cur=con.cursor()
        cur.execute("SELECT promo.idpromo, promo.nompromo, promo.date_debut, promo.date_fin, referentiel.nomref FROM promo, referentiel WHERE promo.idref=referentiel.idref")
        data=cur.fetchall()
        con.commit()

        cur=con.cursor()
        cur.execute("SELECT * FROM referentiel")
        abc = cur.fetchall()
        con.commit()

        return render_template('updatepro.html', promo=data,referentiel=abc)


                        #DEUXIEME ETAPE: UPDATE#############

@app.route('/update1', methods = ['POST','GET'])
def update2():
        if request.method == 'POST':
                id_data = request.form['id_data']
                nompromo = request.form['nompromo']
                date_debut = request.form['date_debut']
                date_fin = request.form['date_fin']
                nomref = int(request.form['Nom Ref'])
                cur = con.cursor()
                cur.execute("""
                UPDATE promo
                SET nompromo=%s, date_debut=%s, date_fin=%s, Idref=%s
                WHERE idpromo=%s """, (nompromo, date_debut,date_fin,nomref,id_data))
                con.commit()
                flash ("Données mises à jour avec succès")

                return redirect(url_for('update1'))

#############################################################################################


################### ANNULER INSCRIPTIONS ########################################################

@app.route('/annuler')
def annuler():
        cur=con.cursor()
        cur.execute("SELECT Idapprenant, matricule, prenom, nom, datenaiss FROM apprenant WHERE statut = 'inscrit'")
        annul=cur.fetchall()
        con.commit()
        return render_template('annulercire.html',cire=annul)

@app.route('/delete1/<string:id_data>', methods = ['GET'])
def delete1(id_data):


    flash("Données supprimées avec succés")
    cur = con.cursor()
    cur.execute("UPDATE apprenant SET statut='annulé' WHERE Idapprenant = %s", (id_data))
    con.commit()
    return redirect(url_for('annuler'))

#########################################################################################

##############################SUSPENDRE###################################################"

@app.route('/suspendre1')
def suspendre1():
        cur=con.cursor()
        cur.execute("SELECT Idapprenant, matricule, prenom, nom, datenaiss FROM apprenant,promo WHERE promo.idpromo=apprenant.idpromo AND statut = 'inscrit'")
        suspend=cur.fetchall()
        con.commit()
        return render_template('suspendre.html',eric=suspend)
        

@app.route('/suspendre2/<string:id_data>', methods = ['GET'])
def suspendre2(id_data):
    flash("Données suspendues avec succés")
    cur = con.cursor()
    cur.execute("UPDATE apprenant SET statut='suspendu' WHERE Idapprenant = %s", (id_data))
    con.commit()
    return redirect(url_for('suspendre1'))


############################################################################################

############################################################################################

if __name__ == "__main__":
    app.run(debug= True)