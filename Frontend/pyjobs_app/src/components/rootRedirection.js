import {useEffect} from 'react';
import {useNavigate} from 'react-router-dom';

export default function RootRedirection() {
    const auth_token = localStorage.getItem('auth_token');
    const expirationTime = localStorage.getItem('expiration');
    const currentTime = new Date().getTime();
	const expirationTimestamp = new Date(expirationTime).getTime();
    const navigate = useNavigate();

    console.log(expirationTime);


    useEffect(() => {
        if (auth_token && expirationTime) {
            if (currentTime < expirationTimestamp) {
                navigate('/jobs', {replace: true})
            }
            else {
                navigate('/login', {replace: true})
            }
        }
        else {
            navigate('/login', {replace: true})
        }
    }, [navigate])
  
    return null;
  }