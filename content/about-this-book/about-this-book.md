## About this Book

This evolution required a workflow as unique as the project itself. Fundamentally, I started developing all of my writing using Scrivener. Scrivener existed well before AI. It's great for organizing your thoughts, organizing your data, organizing your research, organizing your images, and then rendering documents in many different formats. For this work, it is the primary source of truth and the primary rendering engine for any of my working PDFs.

Most of the research, the tables, the graphs, have been created under Cursor 2.0. I developed a platform specifically to author this book. Actually, I didn't just develop it, I developed it pair-programming style, with Cursor AI itself. The workflow is as follows:

1. **Scrivener - Initial Writing & Organization**
   - Basic writing and idea development
   - Document structure setup
   - Contains all research content and images
   - Final "source of truth" for traditional publishing

2. **Scrivener Compile → Markdown → PDF**
   - Scrivener's compile feature creates a master markdown file
   - Piped into Marked 2 where it can be rendered into an appropriate PDF
3. **Physical Review & Red Ink Editing**
   - Read and review the PDF
   - Often make physical copies for red ink editing
   - Track down any hallucinations that the AI might introduce
   - Identify appropriate page breaks

4. **Scrivener Update & Cursor Validation**
   - Update the Scrivener source based on review
   - Grab sections to put into Cursor
   - Cursor agents perform technical validation of claims
   - Validate soundness of code snippets involving actual computations or calculations

5. **Iteration**
   - Repeat the cycle, growing the work organically

The following diagram better illustrates this workflow:

￼![][book-authoring-workflow]

The AI functioned as a research assistant and copywriter. It startles me sometimes how well it knows (or emulates) my intent.

When I got the document to a stage of being complete, I placed it into a [GitHub repo](https://https://github.com/l0r3zz/sloblackswan) for public distribution. As changes are made, GitHub Actions trigger to always have a current copy of the markdown master. One can download the markdown and either drop this into some AI agent for continued processing or evaluation, or render it to a PDF for a more human-readable version.

I invite all readers to submit PRs to the document if you find any inaccuracies. If you take exceptions to some of the assertions or conclusions, please use GitHub issues so that we can hash this out.

This has been a great project, and I think I've found a way to rapidly and accurately transmit some of my insights and wisdom that I've accumulated over my close to 50 years in computing.
{::pagebreak /}


[book-authoring-workflow]: book-authoring-workflow.png