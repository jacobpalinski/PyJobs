import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginSignUp from "./components/loginSignUp";
import Jobs from "./components/jobs";
/* import {useNavigate} from 'react-router-dom'; (redirection in individual component files)
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom' in App.js (for defining routes in return)
import LoginSignUp from "./path" */

function App() {
  return (
    <div>
		<BrowserRouter>
			<Routes>
				<Route path='/login' element={<LoginSignUp />} />
				<Route path='/jobs' element={<Jobs />} />
			</Routes>
		</BrowserRouter>
    </div>
  );
}

export default App;
