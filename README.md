<h1>RAVI Code Snippet Backend</h1>
<p><strong>A Flask-based backend API for storing and managing Python code snippets.</strong> This API is integrated with the <em>RAVI</em> voice assistant, allowing users to add, retrieve, update, and delete Python code snippets through a simple RESTful API.</p>

<h2>🛠️ Setup & Run Locally</h2>
<p>Follow these steps to run the backend locally before deploying:</p>

<pre><code>
git clone https://github.com/your-username/ravi-snippet-backend.git
cd ravi-snippet-backend
pip install -r requirements.txt
python app.py
</code></pre>

<p><strong>Local Server:</strong> <code>http://localhost:10000</code></p>

<h2>📬 API Endpoints</h2>
<p>Below are the API endpoints that interact with your <strong>RAVI Code Snippet</strong> backend:</p>

<h3>1. Add a Code Snippet</h3>
<ul>
    <li><strong>Method:</strong> <code>POST</code></li>
    <li><strong>URL:</strong> <code>/add_snippet</code></li>
    <li><strong>Body (raw > JSON):</strong>
        <pre><code>
{
    "title": "Example Title",
    "description": "A simple Python code snippet",
    "code_snippet": "print('Hello, RAVI!')"
}
        </code></pre>
    </li>
</ul>

<h3>2. List All Snippets</h3>
<ul>
    <li><strong>Method:</strong> <code>GET</code></li>
    <li><strong>URL:</strong> <code>/list_snippets</code></li>
</ul>

<h3>3. Update a Code Snippet</h3>
<ul>
    <li><strong>Method:</strong> <code>PUT</code></li>
    <li><strong>URL:</strong> <code>/update_snippet</code></li>
    <li><strong>Body (raw > JSON):</strong>
        <pre><code>
{
    "id": 1,
    "title": "Updated Title",
    "description": "Updated Python snippet",
    "code_snippet": "print('Updated Snippet!')"
}
        </code></pre>
    </li>
</ul>

<h3>4. Delete a Code Snippet</h3>
<ul>
    <li><strong>Method:</strong> <code>DELETE</code></li>
    <li><strong>URL:</strong> <code>/delete_snippet?id=1</code></li>
</ul>

<h2>🚀 Deploy to Render</h2>

<p><strong>Here’s how to deploy your Flask app on Render:</strong></p>

<ol>
    <li><strong>Push Code to GitHub</strong>  
        <pre><code>
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/ravi-snippet-backend.git
git push -u origin main
        </code></pre>
    </li>
    <li><strong>Create a New Web Service on Render</strong></li>
    <ol>
        <li>Go to <a href="https://render.com" target="_blank">Render</a> and log in.</li>
        <li>Click on "New Web Service".</li>
        <li>Connect your GitHub repository that contains the <code>ravi-snippet-backend</code> project.</li>
        <li>Fill in the build and start commands:
            <ul>
                <li><strong>Build Command:</strong> <code>pip install -r requirements.txt</code></li>
                <li><strong>Start Command:</strong> <code>python app.py</code></li>
            </ul>
        </li>
        <li>Set the environment to Python 3.x (or your required version).</li>
        <li>Select Port <code>10000</code> for the application to run on.</li>
        <li>Click "Deploy" to start the deployment process.</li>
    </ol>

    <li><strong>Obtain the Render URL</strong>
        <p>Once the app is deployed, Render will provide you with a live URL like: <code>https://ravi-snippet-backend.onrender.com</code></p>
    </li>
</ol>

<h2>📱 Integrating with Jetpack Compose using Retrofit</h2>
<p>Now that your backend is deployed on Render, you can connect it to your <strong>Jetpack Compose app</strong> using <strong>Retrofit</strong>. Below is a basic example of how to call your deployed API from the app.</p>

<h3>Retrofit Integration Example</h3>
<pre><code>
interface ApiService {
    @POST("/add_snippet")
    suspend fun addSnippet(@Body snippet: Snippet): Response<ApiResponse>
    @GET("/list_snippets")
    suspend fun getAllSnippets(): Response<List<Snippet>>
    @PUT("/update_snippet")
    suspend fun updateSnippet(@Body snippet: Snippet): Response<ApiResponse>
    @DELETE("/delete_snippet")
    suspend fun deleteSnippet(@Query("id") id: Int): Response<ApiResponse>
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://ravi-snippet-backend.onrender.com")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val apiService = retrofit.create(ApiService::class.java)

// Call the API for adding a snippet
val snippet = Snippet("Example Title", "A sample code snippet", "print('Hello, RAVI!')")
val response = apiService.addSnippet(snippet)
if (response.isSuccessful) {
    // Handle success
} else {
    // Handle error
}
</code></pre>

<h2>🌐 Testing the API on Postman</h2>
<p>Once deployed on Render, use Postman or any API client to test the endpoints:</p>

<ul>
    <li><strong>Add Snippet (POST request):</strong> <code>https://ravi-snippet-backend.onrender.com/add_snippet</code></li>
    <li><strong>List Snippets (GET request):</strong> <code>https://ravi-snippet-backend.onrender.com/list_snippets</code></li>
    <li><strong>Update Snippet (PUT request):</strong> <code>https://ravi-snippet-backend.onrender.com/update_snippet</code></li>
    <li><strong>Delete Snippet (DELETE request):</strong> <code>https://ravi-snippet-backend.onrender.com/delete_snippet?id=1</code></li>
</ul>

<h2>📂 Project Structure</h2>
<pre><code>
ravi-snippet-backend/
├── app.py              # Flask application
├── requirements.txt    # Dependencies
└── data/
    └── ravi.db         # SQLite3 database (auto-created)
</code></pre>

<h2>✅ Tech Stack</h2>
<ul>
    <li>Python 3.x</li>
    <li>Flask</li>
    <li>SQLite3</li>
    <li>Render (for cloud deployment)</li>
</ul>

<h2>🧑‍💻 Support</h2>
<p>For any queries or collaboration ideas, feel free to reach out via <a href="[https://www.linkedin.com/in/aditya-<your-profile](https://www.linkedin.com/in/aditya-patil-a7743a292/)>" target="_blank">LinkedIn</a> or email.</p>

<footer>
    <p><em>Made with ❤️ by Aditya — Building the Future of AI.</em></p>
</footer>
