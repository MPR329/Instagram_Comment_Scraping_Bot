const puppeteer = require('puppeteer');
const fs = require('fs');

// Définir les infos sur les comptes instagram utilisés

const nom_utilisateur = "entrer le nom d'utilisateur instagram";
const pwd = "entrer le password instagram";

// Le site instagram 
const instagram = "https://www.instagram.com/";

//Le lien du post sur lequel on veut scraper les commentaires


var post = "https://www.instagram.com/p/CW_ysEuo2wB/";
var regexURL = /https:\/\/www.instagram.com\/p\/(.*)\//;
var idURL = post.match(regexURL);
var idMatch = idURL[1];
console.log(idMatch)


// Définir les paramètres du browser et des pages que l'on va ouvrir
let browser = null;
let page = null;

(async () => {
    browser = await puppeteer.launch({
        headless: false, args: [
            '--start-maximized',
            '--enable-automation',
        ],
    });
    page = await browser.newPage();
    page.setViewport({
        width: 1920,
        height: 1080,
    });

    function organizeHTML(attr){
        // REGEX
        let nomUtilisateur = /href="\/(.*?)\/" tabindex="0"/;
        let dateTime = /datetime="(.*?)"/;
        let nbLikes = />([^"]*?)likes/;
        let nbReplies = /replies \((.*?)\)/;
        let commentaire_regex = /<div class="MOdxS "><span(?:.*?)>(?:<a(?:.*?)<\/a> )*(.*?)</;
        let tags = /(@.*?)<\/a>/g;
        let hashTags = /href="\/explore\/tags\/(.*?)\//g;
        let verified = /title="Verified"/;

        for (j = 0; j < attr.length; j++) {
            //console.log(j);

            let commentHTML = attr[j];

            // Les matchs dans le regex dans le html
            // le nom d'utilisateur
            let matchNomUtilisateur = commentHTML.match(nomUtilisateur);
            let username = matchNomUtilisateur[1];
            // Le dateTime, puis chacun séparé
            let matchDateTime = commentHTML.match(dateTime);
            let string = matchDateTime[1]
            let dateAndTime = /(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})/;
            let matchDateAndTime = string.match(dateAndTime);
            let date = matchDateAndTime[1]
            let time = matchDateAndTime[2]
            // Le commentaire
            let matchCommentaire = commentHTML.match(commentaire_regex);
            let commentaire = matchCommentaire[1];
            // Les tags
            let matchTags = [...commentHTML.matchAll(tags)];
            // Les hashtags
            let matchHashTags = [...commentHTML.matchAll(hashTags)];
            // Le statut du compte (i.e : verified or not)
            let matchVerified = verified.test(commentHTML);
            // Le ID du commentaire (à partir du counter)
            let id = j.toString();
            // Le nombre de likes (si aucun on le set à 0)
            let matchNbLikes = commentHTML.match(nbLikes);
            if (matchNbLikes != null) {
                var likes = matchNbLikes[1]
            } else {
                var likes = 0;
            }
            
            // Le nombre de replies (si aucun on le set à 0)
            let matchNbReplies = commentHTML.match(nbReplies);
            if (matchNbReplies != null) {
                var replies = matchNbReplies[1]
            } else {
                var replies = 0;
            }
            //console.log("NB OF REPLIES = " + replies);
            // S'il y a des tags on les mets dans une liste sinon on indique 0
            if (matchTags.length) {
                var tagsList = [];
                matchTags.forEach(x => tagsList.push(x[1]));
            } else {
                var tagsList = 0;
            }
            // S'il y a des hashtags on les mets dans une liste sinon on indique 0
            if (matchHashTags.length) {
                var hashtagsList = []
                matchHashTags.forEach(x => hashtagsList.push(x[1]));
            } else {
                var hashtagsList = 0;
            }

            // On construit ici l'objet "commentInfo" qui rassemble toutes les infos trouvées ci-dessus avec les regex ...
            let commentInfo = {
                USERNAME: username,
                ID: id,
                DATE: date,
                TIME: time,
                LIKES: likes,
                REPLIES: replies,
                COMMENTS: commentaire,
                TAGS: tagsList,
                HASHTAGS: hashtagsList,
                ACCOUNT_STATUS: matchVerified
            }
            // ... puis on l'ajoute à la liste "comments"
            comments.push(commentInfo);
        }
        console.log("Length of list : " + comments.length)
    }
    
    console.time('TOTAL SCRAPING TIME');
    // On utilise "try" ici pour pouvoir sauvegarder les résultats du scraping même en cas d'erreurs.
    try {
        console.time('Connecting to instagram');
        await page.bringToFront();

        // Aller sur le site  d'instagram
        await page.goto(instagram, { waitUntil: 'networkidle2' });
        console.log("\nOn the instagram website");
        await page.waitForTimeout(2000);

        // Cliquer sur le bouton pour accepter les cookies et attendre
        const cookies_accept = await page.$x("//button[contains(text(), 'Only allow essential cookies')]");
        await cookies_accept[0].click();
        console.log("Accepted cookies")
        await page.waitForTimeout(4000);

        // Attendre qu'il soit possible d'entrer le username et mot de passe puis le faire
        await page.waitForSelector('input[name="username"]');
        await page.type('input[name="username"]', nom_utilisateur, { delay: 60 });
        console.log("Entered username");
        await page.type('input[name="password"]', pwd, { delay: 50 });
        console.log("Entered password");
        await page.waitForTimeout(2000);

        // Cliquer sur le bouton login
        await page.click('button[type="submit"]');
        console.log("Clicked on login button")
        await page.waitForTimeout(4000);

        // Aller sur le lien du post concerné.
        await page.goto(post, { waitUntil: 'networkidle2' });
        console.log("\nOn the instagram website");

        console.timeEnd('Connecting to instagram')


        // La liste dans laquelle on va stocker les commentaires sous forme d'objets
        var comments = [];
        var times = [];
        
        var startTime=new Date().getTime();
        var counter = 0;

        while (await page.waitForSelector('svg[aria-label="Load more comments"]')!=null) {
            // Si class="GdeD6 AzWhO" est présent : enlever de l'html

            let endTime=new Date().getTime();
            let time = endTime-startTime;
            times.push(time)
            
            startTime=new Date().getTime();

            counter = counter + 1;

            console.timeEnd('Scraping newly loaded comments');
            console.time('Scraping newly loaded comments');
            console.log('Stage : |' + counter + '|')

            //let cible = document.getElementsByClassName("GdeD6 AzWhO");
            let attr = await page.$$eval(".Mr508", el => el.map(x => x.innerHTML));
            //let cible = await page.$$eval(".GdeD6 AzWhO", el => el.map(x => x.innerHTML));
            //console.log(cible.length);
            console.log("Length of added comments : " + attr.length + "\n");

    
            // INSERT FUNC HERE
            await organizeHTML(attr);

            await page.evaluate(() => {
                let comments = document.querySelectorAll('.Mr508');
                comments.forEach(comment => {comment.remove();});
            });

            await page.click('svg[aria-label="Load more comments"]');
            
        }
        
    } catch (err) {
       
        // Data which will write in a file.
        var commentJSON = JSON.stringify(comments);
        fs.writeFile(idMatch + '_COMMENTS.txt', commentJSON, (err) => {
            if (err) throw err;
        })
    
        console.log("\n---------------------------\n");
        console.log("Document successfuly written");
        console.log("\n---------------------------\n");

        var TIMEJSON = JSON.stringify(times);
        fs.writeFile(idMatch + '_TIMELOG.txt', TIMEJSON, (err) => {
            if (err) throw err;
        })
        console.log("SAVED TIME LOG")
        console.log(comments.length)
        console.timeEnd('TOTAL SCRAPING TIME');

    
        throw err;
    }
        
})();
