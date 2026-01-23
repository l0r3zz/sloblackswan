## About this Book

This revelation required a workflow as unique as the project itself. Fundamentally, I started developing all of my writing using Scrivener. Scrivener existed well before AI. It's great for organizing your thoughts, organizing your data, organizing your research, organizing your images, and then rendering documents in many different formats. For this work, it started as the primary source of truth and the primary rendering engine for any of my working PDFs. But as I started to use AI tools, specifically Cursor, I shifted to authoring in markdown, which seems to be becomming the defacto format for all minimally structured text.

Most of the research, the tables, the graphs, have been created under Cursor 2.0. I developed a platform specifically to author this book. Actually, I didn't just develop it, I developed it pair-programming style, with Cursor AI itself. The workflow is as follows:

**Scrivener - Initial Writing & Organization**

   - Basic writing and idea development
   - Document structure setup
   - Contains all research content and images
   - Final "source of truth" for traditional publishing

**Scrivener Compile → Markdown → PDF**

   - Scrivener's compile feature creates a master markdown file
   - Piped into Marked 2 where it can be rendered into an appropriate PDF

**Physical Review & Red Ink Editing**

   - Read and review the PDF
   - Often make physical copies for red ink editing

**Scrivener Update & Cursor Validation**

   - Update the Scrivener source based on review
   - Grab sections to put into Cursor
   - Cursor agents perform technical validation of claims
   - Validate soundness of code snippets involving actual computations or calculations
   - Track down any hallucinations that might show up

**Iterations in Cursor**

   - I developed some scaffolding with Cursor, tailored to the production of this book
   - I stopped updating Scrivener so much and just made changes using the scaffolding 
   - [SLOBLACKSWAN-Cursor](https://github.com/l0r3zz/sloblackswan-cursor) became the primary authoring tool
   - A generic form that is ready for you to try yourself, can be found at [Cursor-Writing-Assistant](https://github.com/l0r3zz/Cursor-Writing-Assistant)

**Create and push a PR to github**

   - Any changes made in a forked source are rolled into a PR and merged into *main*
   - Automated a github workflow to automatically produce an md file, pdf and update the website
   - I evaluate any PRs and make a decision on whether to merge as is, "squash",or "cherry pick" commits
   - changes are merged back into the Scrivener source of truth as checkpoints

**Iteration**
   - Interact, Discuss, Improve
   - Repeat the cycle, growing the work organically

The following diagram better illustrates this workflow:

￼![][book-authoring-workflow]

The AI functioned as a research assistant and copywriter. It startles me sometimes how well it knows (or emulates) my intent. Still, one cannot just "let it rip", I've found a couple of hallucinations and the perpetuations of some "myths", fortunately myself, along with a couple of my reviewers caught some of them. I'm sure there are still some lurking deep inside the pages.

Now that the document is released, I've  placed it into a [GitHub repo](https://github.com/l0r3zz/sloblackswan) for public distribution and commenting. As changes are made, GitHub Actions trigger to always have a current copy of the markdown master. One can download the markdown and either drop this into some AI agent for continued processing or evaluation, or render it to a PDF for a more human-readable version.

I invite all readers to submit PRs to the document if you find any inaccuracies. If you take exceptions to some of the assertions or conclusions, please use GitHub issues so that we can hash this out.

This has been a great project, and I think I've found a way to rapidly and accurately transmit some of my insights and wisdom that I've accumulated over my 40+ years in computing.
{::pagebreak /}


[book-authoring-workflow]: book-authoring-workflow.jpg