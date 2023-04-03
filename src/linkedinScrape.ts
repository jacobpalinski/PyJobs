import * as cheerio from 'cheerio';
import fetch from 'node-fetch';

class linkedinScraper {
    // Programming languages , databases and clodu providers to search for when parsing html
    static programmingLanguages: readonly string[] = ["'Python'","'Javascript'", "'TypeScript'"];
    static databases: readonly string[] = ["MySQL","PostgreSQL","SQLite","MongoDB","Microsoft SQL Server",
    "MariaDB","Firebase","ElasticSearch","Oracle","DynamoDB"];
    static cloudProvider: readonly string[] = ["Amazon Web Services","AWS","Azure","Google Cloud", "GCP"];
    static location: readonly string[] = ['Sydney'] // Other locations to be added later once code with AWS works

    // Generate URL based on city
    static generateURL(city: string, startNum : number): string {
        const url = `https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=${city}&f_TPR=r86400&position=1&pageNum=0&start=${startNum}`;
        return url;
    }


}

export {linkedinScraper}