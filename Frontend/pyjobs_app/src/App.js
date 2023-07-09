import { BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import LoginSignUp from "./components/loginSignUp";
import Jobs from "./components/jobs";
import RootRedirection from "./components/rootRedirection";
/* import {useNavigate} from 'react-router-dom'; (redirection in individual component files)
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom' in App.js (for defining routes in return)
import LoginSignUp from "./path" */

function App() {
	const isAuthenticated = () => {
		const auth_token = localStorage.getItem('auth_token');
		const expirationTime = localStorage.getItem('expiration');
		const currentTime = new Date().getTime();
		const expirationTimestamp = new Date(expirationTime).getTime();
	
		if (auth_token && expirationTime) {
			return currentTime < expirationTimestamp;
		}
		return false;
	};

	const PrivateRoute = () => {
		return isAuthenticated() ? (
			<Jobs />
		) : (
			<Navigate to='/login' replace={true}/>
		);		
	};

  return (
    <div>
		<BrowserRouter>
			<Routes>
				<Route path='/' element={<RootRedirection />} />
				<Route path='/login' element={<LoginSignUp />} />
				<Route path='/jobs' element= {<PrivateRoute />} />
			</Routes>
		</BrowserRouter>
    </div>
  );
}

export default App;
