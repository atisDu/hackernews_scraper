import React from 'react';
import axios from 'axios';
import $ from 'jquery'; //Dep. Datatables
import 'datatables.net-dt';
import './App.css';
import "@radix-ui/themes/styles.css";
import { Slider } from "radix-ui"; // Divu punktu slideris, lai atlasītu lapas nr.
import "./styles.css";
import { Box, Card } from '@radix-ui/themes';

// TODO:
// (X) izdomāt loģiku, kā labāk scrapot ierakstus, piemēram, no 10 lapām uzreiz, nevis pa vienai (IR)
// () Kā no datatables dabūt page mainīgo, lai varētu views ielikt iekšā scriptā

class App extends React.Component {
    state = {
        posts: [],
        loading: false,
        error: null,
        sliderValue: [0, 10], //sliderim sākotnējās vērtības ir 0 un 10
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

        

        //Ja jau eksistē, tad tikai atjaunina datus
        if ($.fn.DataTable.isDataTable('#postsTable')) {
            const table = $('#postsTable').DataTable();
            table.clear();
            table.rows.add(this.state.posts);
            table.draw(false);  // atstāj to pašu lapu
            return;
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
            order: [[3, 'desc']], //Jaunākie ieraksti pirmie
            searching: true,
            ordering: true,
            responsive: true,
            pageLength: 10,
            lengthMenu: [10, 25, 50, 100],
            destroy: true
        });
        /*
        //klausās lpp nr.
        $('#postsTable').on('page.dt', () => {
        const current = table.page();
        console.log("Page changed to:", current + 1);
        localStorage.setItem('postsTablePage', current);
        });

        $('#postsTable').on('length.dt', function () {
        const table = $('#postsTable').DataTable();
        console.log("Rows per page is now:", table.page.len());
        });
        */
    }

    handleScrape = () => {
        this.setState({ loading: true });
        const [start_page_nr, end_page_nr] = this.state.sliderValue; //Dabū jau no stāvokļa lapu nr.
        axios.post('http://localhost:8000/posts/scrape/', { start_page: start_page_nr, end_page: end_page_nr })
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
        const [start_page_nr, end_page_nr] = this.state.sliderValue; //Dabū jau no stāvokļa lapu nr.
        axios.post('http://localhost:8000/posts/update_scores/', { start_page: start_page_nr, end_page: end_page_nr })
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

    handleSliderChange = (newValue) => {
        this.setState({ sliderValue: newValue });
    }

    render() {
        const { loading, error, sliderValue } = this.state;

        return (
            <div className="app-container">
                <h1>HackerNews scraper</h1>

            <Box>
                <Card>
                    
                <form>
		    <Slider.Root className="SliderRoot" defaultValue={[0, 10]} max={50} step={1} minStepsBetweenThumbs={1} onValueChange={this.handleSliderChange}>
			<Slider.Track className="SliderTrack">
				<Slider.Range className="SliderRange" />
			</Slider.Track>
			<Slider.Thumb className="SliderThumb" aria-label="Volume" />
            <Slider.Thumb className="SliderThumb" aria-label="Volume" />
		</Slider.Root>
	    </form> 
         <p ref={this.sliderDisplayRef}>
                Scrape pages: {sliderValue[0]} to {sliderValue[1]}
                </p>
                
                 <div className="button-container">
                    <button 
                        onClick={() => this.handleScrape()} //Nodod slidera vērtības scrape service scriptam
                        disabled={loading}
                        className="btn btn-scrape"
                    >
                        {loading ? 'Loading...' : 'Scrape New Posts'}
                    </button>
                    
                    <button 
                        onClick={() => this.handleUpdateScores()} 
                        disabled={loading}
                        className="btn btn-update"
                    >
                        {loading ? 'Loading...' : 'Update Scores'}
                    </button>

                   
                </div>

                </Card>
            </Box>
            
                <br></br>

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