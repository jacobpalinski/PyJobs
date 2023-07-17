import {useEffect} from 'react';
import {useNavigate} from 'react-router-dom';

export default function RootRedirection() {
    const authToken = localStorage.getItem("authToken");
    const expirationTime = localStorage.getItem("expirationTime");
    const currentTime = new Date().getTime();
	const expirationTimestamp = new Date(expirationTime).getTime();
    const navigate = useNavigate();


    useEffect(() => {
        if (authToken && expirationTime) {
            if (currentTime < expirationTimestamp) {
                navigate("/jobs", {replace: true});
            }
            else {
                navigate("/login", {replace: true});
            }
        }
        else {
            navigate("/login", {replace: true});
        }
    }, [navigate]);
  
    return null;
  }