import {test, expect} from '@jest/globals'
import {sumNum} from '../src/linkedinScrape'

test('sum correct', () => {
    expect(sumNum(2,3)).toEqual(5)
} )