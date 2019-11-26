
var A_trouver = Math.round(Math.random()*500)
var Nombre_donner = prompt("Est-ce que tu peux m'indiquer un chiffre ?")
var Nombre_essaie = 0
var phrase = ""
while(A_trouver != Nombre_donner){
    Nombre_essaie = Nombre_essaie+1
    if(Nombre_donner > A_trouver){
        phrase = "Ton Chiffre est trop grand ! tu es à ton "+ Nombre_essaie + " essaies"
        Nombre_donner = prompt(phrase)
    }
    else {
        phrase = "Ton Chiffre est trop petit ! tu es à ton "+ Nombre_essaie + " essaies"
        Nombre_donner = prompt(phrase)
    }
}
Nombre_essaie = Nombre_essaie+1
phrase = "Tu as bien trouver le chiffre en " + Nombre_essaie + " d'essaie"
alert(phrase)






