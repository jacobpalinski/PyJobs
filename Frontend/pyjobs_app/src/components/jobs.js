import {useEffect, useState} from 'react';
import '../css/jobs.css';
import Pagination from './pagination';
import Select from "react-select";
import AsyncSelect from "react-select/async";

export default function Jobs() {
    let [data, setData] = useState([]);
    const [locations, setLocations] = useState([]);
    const [companies, setCompanies] = useState("");
    const [group, setGroup] = useState("");
    const [datePosted, setDatePosted] = useState(0);
    const [jobTitle, setJobTitle] = useState("");
    const [selectedDatabases, setSelectedDatabases] = useState([]);
    const [selectedCloudProviders, setSelectedCloudProviders] = useState([]);
    const databases = [
        {value: "MySQL", label: "MySQL"},
        {value: "PostgreSQL", label: "PostgreSQL"},
        {value: "SQLite", label: "SQLite"},
        {value: "MongoDB", label: "MongoDB"},
        {value: "MS SQL", label: "MS SQL"},
        {value: "SQL Server", label: "SQL Server"},
        {value: "Maria DB", label: "Maria DB"},
        {value: "Firebase", label: "Firebase"},
        {value: "ElasticSearch", label: "ElasticSearch"},
        {value: "Oracle", label: "Oracle"},
        {value: "DynamoDB", label: "DynamoDB"}
    ];
    const cloudProviders = [
        {value: "Amazon Web Services", label: "Amazon Web Services"},
        {value: "AWS", label: "AWS"},
        {value: "Azure", label: "Azure"},
        {value: "Google Cloud", label: "Google Cloud"},
        {value: "GCP", label: "GCP"}
    ];
    const [currentPage, setCurrentPage] = useState(1);
    const[postsPerPage] = useState(3);

    const indexofLastPost = currentPage * postsPerPage;
    const indexofFirstPost = indexofLastPost - postsPerPage;
    const currentPosts= data.slice(indexofFirstPost,indexofLastPost);
    const howManyPages = Math.ceil(data.length/postsPerPage);

    console.log(data);

    //custom data
    useEffect(() => {
        const fetchjobData = async () => {
            // Base URL
            let url = 'http://127.0.0.1:5000/job_data/jobData';
            // Query parameters based on selected values
            const queryParams = [];

            if (locations) {
                locations.forEach( (location) => {
                    queryParams.push(`location=${location}`);
                })
            }

            if (companies) {
                companies.forEach( (company) => {
                    queryParams.push(`company=${company}`);
                } )
            }

            if (group) {
                queryParams.push(`group=${group}`);
            }

            if (datePosted) {
                queryParams.push(`days_old=${datePosted}`);
            }

            if (jobTitle) {
                queryParams.push(`jobTitle=${jobTitle}`);
            }

            if (selectedDatabases) {
                selectedDatabases.forEach( (database) => {
                    queryParams.push(`database=${database}`);
                })
            }

            if (selectedCloudProviders) {
                selectedCloudProviders.forEach( (provider) => {
                    queryParams.push(`cloud=${provider}`);
                })
            }

            console.log(queryParams);

            if (queryParams.length > 0) {
                url += `?${queryParams.join('&')}`;
            }

            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                const data = await response.json();
                setData(data);
            } catch (error) {
                console.error('Error retrieving data', error);
            }
        };
        fetchjobData();
    }, [locations, companies, group, datePosted, jobTitle, selectedDatabases, selectedCloudProviders]);

    // select onchange function getting option selected value and save inside state variable
    function handleLocationsChange (e) {
        setLocations(e.map(location => location.value));
    };

    function handleCompaniesChange (e) {
        setCompanies(e.map(company => company.value));
    }

    function handleGroupChange (e) {
        setGroup(e.target.value);
    }

    function handleDatePosted (e) {
        setDatePosted(e.target.value);
    }

    function handleJobTitle (e) {
        setJobTitle(e.target.value);
    }

    function handleSelectedDatabases (e) {
        setSelectedDatabases(e.map(database => database.value));
    }

    function handleSelectedCloudProviders (e) {
        setSelectedCloudProviders(e.map(provider => provider.value));
    }

    const loadLocationsOptions = async (searchValue, callback) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/job_data/jobData?location=${searchValue}`);
            const data = await response.json();
            const uniqueLocations = Array.from(new Set(data.map(job => job.location)));
            const options = uniqueLocations.map(location => ({ value: location, label: location }));
            callback(options);
        } catch (error) {
            console.error('Error retrieving location data', error);
            return [];
        }
    }

    const loadCompaniesOptions = async (searchValue, callback) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/job_data/jobData?company=${searchValue}`);
            const data = await response.json();
            const uniqueCompanies = Array.from(new Set(data.map(job => job.company)));
            const options = uniqueCompanies.map(company => ({ value: company, label: company}));
            callback(options);
        } catch (error) {
            console.error('Error retrieving location data', error);
            return [];
        }
    }

    //hooks calls after rendering select state
    /*useEffect(() => {
        // Doing filtration based on location
        const jobData = initialData.filter(jobData => jobData.location === location 
            && jobData.company === company 
            && jobData.group === group);
        setData(jobData);
    }, [location, company, group, datePosted])*/

    return (
        <div>
            <div className="jobs-container">
                <h1 className="jobs-header">Jobs</h1>
                <div className="filters">
                    <div className="date-posted">
                        <label className="form-label">Date Posted</label>
                            <select id="date-posted" onChange={handleDatePosted} className="form-select">
                                <option value={1}>&lt; 1 day</option>
                                <option value="Graduate Software Developer (Python)">Graduate Software Developer (Python)</option>
                            </select>
                    </div>
                    <div className="locations">
                        <label className="form-label">Locations</label>
                        <AsyncSelect defaultOptions loadOptions={loadLocationsOptions} onChange={handleLocationsChange} isMulti />
                    </div>
                    <div className="company">
                        <label className="form-label">Companies</label>
                        <AsyncSelect defaultOptions loadOptions={loadCompaniesOptions} onChange={handleCompaniesChange} isMulti />
                    </div>
                    <div className="group">
                        <label className="form-label">Group</label>
                        <select id="group" onChange={handleGroupChange} className="form-select">
                            <option value="Software Engineering / Development">Software Engineering / Development</option>
                            <option value="Data Science / Engineering">Data Science / Engineering</option>
                        </select>
                    </div>
                    <div className="databases">
                        <label className="form-label">Databases</label>
                        <Select options={databases} onChange={handleSelectedDatabases} isMulti/>
                    </div>
                    <div className="cloud-providers">
                        <label className="form-label">Cloud Providers</label>
                        <Select options={cloudProviders} onChange={handleSelectedCloudProviders} isMulti/>
                    </div>
                    <div className="jobtitle">
                        <label className="form-label">Job Title</label>
                        <input type="text" name="search" onChange={handleJobTitle} placeholder="Job Title" />
                    </div>
                </div>
                {data.length !== 0 ? (<div className="table-container">
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col">Date Posted</th>
                            <th scope="col">Location</th>
                            <th scope="col">Company</th>
                            <th scope="col">Group</th>
                            <th scope="col">Job Title</th>
                            <th scope="col">Databases</th>
                            <th scope="col">Cloud Providers</th>
                            <th scope="col">Link</th>
                        </tr>
                    </thead>
                    <tbody>
                        { // calling the state variable to filter data inside table
                        currentPosts.map(function({datePosted,location,company,group,jobTitle,databases,cloudProviders,link})
                        {
                            return (
                                <tr>
                                    <td>{datePosted}</td>
                                    <td>{location}</td>
                                    <td>{company}</td>
                                    <td>{group}</td>
                                    <td>{jobTitle}</td>
                                    <td>{databases.join(', ')}</td>
                                    <td>{cloudProviders.join(', ')}</td>
                                    <td><a href={link}>{link}</a></td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
                <Pagination pages = {howManyPages} setCurrentPage={setCurrentPage}/>
            </div>
             ) : (<p>No jobs exist for given filters</p>)}
        </div>
    </div>
    );
}