import React from 'react';
import axios from 'axios';
import $ from 'jquery'; //Dep. Datatables
import 'datatables.net-dt';
import './App.css';

// TODO:
// (X) izdomāt loģiku, kā labāk scrapot ierakstus, piemēram, no 10 lapām uzreiz, nevis pa vienai (IR)
// () Kā no datatables dabūt page mainīgo, lai varētu views ielikt iekšā scriptā

class App extends React.Component {

    state = {
        posts: [],
        loading: false,
        error: null,
        dataTable: null,
    }

    componentDidMount() {
        this.fetchPosts();
    }

    fetchPosts = () => {
        axios.get('http://localhost:8000/') //Visu fetchojam ar axios serializāciju no django rest api
            .then(res => {
                const postsData = res.data.data || res.data;
                this.setState({
                    posts: postsData,
                    error: null
                }, () => {
                    this.initializeDataTable();
            });
        })
            .catch(err => {
                this.setState({
                    error: 'Failed to fetch posts, is Django up?'
                });
            })
    }

    //Loģika lai inicializētu DataTable
    initializeDataTable = () => {
        //Iznīcina ja eksistē jau
        if ($.fn.DataTable.isDataTable('#postsTable')) {
            $('#postsTable').DataTable().destroy();
        }

        //Uztaisa jaunu
        $('#postsTable').DataTable({
            data: this.state.posts,
            columns: [
                { 
                    data: 'title',
                    title: 'Title',
                    render: function(data) {
                        return '<strong>' + data + '</strong>';
                    }
                },
                { 
                    data: 'score',
                    title: 'Score'
                },
                { 
                    data: 'url',
                    title: 'URL',
                    render: function(data) {
                        return '<a href="' + data + '" target="_blank">Link</a>';
                    }
                },
                { 
                    data: 'posted_at',
                    title: 'Posted At',
                    render: function(data) {
                        return new Date(data).toLocaleString();
                    }
                }
            ],
            paging: true,
            searching: true,
            ordering: true,
            responsive: true,
            pageLength: 10,
            lengthMenu: [10, 25, 50, 100],
            destroy: true
        });
    }

    handleScrape = () => {
        this.setState({ loading: true });
        
        axios.post('http://localhost:8000/posts/scrape/', { page: 1 })
            .then(res => {
                this.setState({
                    posts: res.data,
                    loading: false,
                    error: null
                }, () => {
                    this.initializeDataTable();
                });
            })
            .catch(err => {
                this.setState({
                    error: 'Failed to scrape data',
                    loading: false
                });
            })
    }

    handleUpdateScores = () => {
        this.setState({ loading: true });
        
        axios.post('http://localhost:8000/posts/update_scores/', { page: 1 })
            .then(res => {
                this.setState({
                    posts: res.data,
                    loading: false,
                    error: null
                }, () => {
                    this.initializeDataTable();
                });
            })
            .catch(err => {
                this.setState({
                    error: 'Failed to update scores',
                    loading: false
                });
            })
    }

    render() {
        const { loading, error } = this.state;

        return (
            <div className="app-container">
                <h1>HackerNews scraper</h1>
                
                <div className="button-container">
                    <button 
                        onClick={this.handleScrape} 
                        disabled={loading}
                        className="btn btn-scrape"
                    >
                        {loading ? 'Loading...' : 'Scrape New Posts'}
                    </button>
                    
                    <button 
                        onClick={this.handleUpdateScores} 
                        disabled={loading}
                        className="btn btn-update"
                    >
                        {loading ? 'Loading...' : 'Update Scores'}
                    </button>

                    <button 
                        onClick={this.fetchPosts} 
                        disabled={loading}
                        className="btn btn-refresh"
                    >
                        {loading ? 'Loading...' : 'Refresh'}
                    </button>
                </div>

                {error && <div className="error-message">{error}</div>}

                <div className="table-container">
                    <table id="postsTable" className="display">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Score</th>
                                <th>URL</th>
                                <th>Posted At</th>
                            </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>
        );
    }
}

export default App;