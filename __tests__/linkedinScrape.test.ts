import {test, expect} from '@jest/globals';
import * as fs from 'fs';
import * as cheerio from 'cheerio';

// Mock HTML Data
const mockHTML = fs.readFileSync('./Sydney _Python_ OR _Javascript_ OR _Typescript_ Jobs_Mock.html');

// Load HTML into Cheerio
const $ = cheerio.load(mockHTML);

