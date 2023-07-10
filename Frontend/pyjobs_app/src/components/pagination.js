import {useEffect, useState} from 'react';
import '../css/pagination.css';

export default function Pagination( {pages, setCurrentPage}) {
    const numberOfPages = []
    for (let i = 1; i <= pages; i++) {
        numberOfPages.push(i)
    }

    // Current active button number
    const [currentButton, setCurrentButton] = useState(1)

    // Array of buttons what we see on the page
    const [arrOfCurrButtons, setArrofCurrButtons] = useState([]);

    useEffect( () => {
        let tempNumberOfPages = [...arrOfCurrButtons]

        let dotsInitial = '...';
        let dotsLeft = '... ';
        let dotsRight = ' ...';

        if (numberOfPages.length < 6) {
            tempNumberOfPages = numberOfPages
        }

        else if (currentButton >= 1 && currentButton <= 3) {
            tempNumberOfPages = [1, 2, 3, 4, dotsInitial, numberOfPages.length]
        }

        else if (currentButton === 4) {
            const sliced = numberOfPages.slice(0,5);
            tempNumberOfPages = [...sliced, dotsInitial, numberOfPages.length]
        }

        else if (currentButton > 4 && currentButton < numberOfPages.length - 2) {
            const sliced1 = numberOfPages.slice(currentButton - 2, currentButton)
            const sliced2 = numberOfPages.slice(currentButton, currentButton + 1)
            tempNumberOfPages = ([1, dotsLeft, ...sliced1, ...sliced2, dotsRight, numberOfPages.length])
        }

        else if (currentButton > numberOfPages.length - 3) {
            const sliced = numberOfPages.slice(numberOfPages.length - 4)
            tempNumberOfPages = ([1,dotsLeft, ...sliced])
        }

        else if (currentButton === dotsInitial) {
            setCurrentButton(arrOfCurrButtons[arrOfCurrButtons.length - 3] + 1)
        }

        else if (currentButton === dotsRight) {
            setCurrentButton(arrOfCurrButtons[3] + 2)
        }

        else if (currentButton === dotsLeft) {
            setCurrentButton(arrOfCurrButtons[3] - 2)
        }

        setArrofCurrButtons(tempNumberOfPages);

        if (pages < currentButton) {
            setCurrentButton(1)
            setCurrentPage(currentButton);
        } else {
            setCurrentPage(currentButton);
        }

    }, [currentButton, pages]);

    return (
        <div className="pagination-container">
            <a href="#" className={`${currentButton === 1 ? 'disabled' : ''}`} onClick={() => setCurrentButton(prev => prev <= 1 ? prev: prev - 1)}>
                Prev
            </a>

            {arrOfCurrButtons.map(((item, index) => {
                return <a href="#" key={index} className={`${currentButton === item ? 'active' : ''}`} onClick={() => setCurrentButton(item)}>
                    {item}
                </a>
            }))}

            <a href="#" className={`${currentButton === numberOfPages.length ? 'disabled' : ''}`} onClick={() => setCurrentButton(prev => prev >= numberOfPages.length ? prev : prev + 1)}>
                Next
            </a>
        </div>
    );
}