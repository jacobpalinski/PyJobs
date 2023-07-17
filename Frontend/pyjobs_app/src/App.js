import { BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import LoginSignUp from "./components/loginSignUp";
import Jobs from "./components/jobs";
import RootRedirection from "./components/rootRedirection";

function App() {
	const isAuthenticated = () => {
		const authToken = localStorage.getItem("authToken");
		const expirationTime = localStorage.getItem("expirationTime");
		const currentTime = new Date().getTime();
		const expirationTimestamp = new Date(expirationTime).getTime();
	
		if (authToken && expirationTime) {
			return currentTime < expirationTimestamp;
		}
		return false;
	};

	const PrivateRoute = () => {
		return isAuthenticated() ? (
			<Jobs />
		) : (
			<Navigate to="/login" replace={true}/>
		);		
	};

  return (
    <div>
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<RootRedirection />} />
				<Route path="/login" element={<LoginSignUp />} />
				<Route path="/jobs" element= {<PrivateRoute />} />
			</Routes>
		</BrowserRouter>
    </div>
  );
}

export default App;
