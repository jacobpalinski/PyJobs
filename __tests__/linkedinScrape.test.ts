import {test, expect} from '@jest/globals';
import * as fs from 'fs';
import * as cheerio from 'cheerio';
import {linkedinScraper} from '../src/linkedinScrape';

// Mock HTML Data
const mockHTML = fs.readFileSync('__tests__/Sydney _Python_ OR _Javascript_ OR _Typescript_ Jobs_Mock.html');

// Load HTML into Cheerio
const $ = cheerio.load(mockHTML);

// Test URL is generated correctly
test ('generate URL', () => {
    const actual = linkedinScraper.generateURL(linkedinScraper.location[0], 0);
    const expected = 'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0';
    expect(actual).toEqual(expected);
})

