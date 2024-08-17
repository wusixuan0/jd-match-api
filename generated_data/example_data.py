

promt="""
Generate a list of 50 complete HTML resumes. The output should be a list of full HTML document, including <html>, <head>, and <body> tags. Do not return explanation or any other information.
focusing on candidate qualifications, preferences, career goals, and suitability. Ensure diversity in experience levels, backgrounds, and skills.

Candidate Details:
- Locations: Toronto, Vancouver, Montreal, Calgary, and other major Canadian cities
- Job titles: Data Engineer, Data Scientist, Machine Learning Engineer, Software Engineer, Data Analyst, Business Intelligence Analyst, Paid Search Specialist, Paid Media Specialist, Paid Social Specialist.

Additional Instructions:
1. diversity matters! Vary experience levels.
2. Ensure diversity in educational backgrounds, including representation from immigrant communities.
3. Make resumes ATS-friendly by using relevant keywords for each job title.
4. Include a mix of full-time, part-time, internship, and volunteer experiences in the work history.
5. Keep content concise, equivalent to 1-2 pages in a traditional resume format.
6. Omit personal information (name, contact details, etc.).
7. Use action verbs and quantify achievements where possible in work experiences and projects.
8. Vary the amount of detail in work experiences, educational entries, and projects across resumes.
9. Include both common and niche skills relevant to each job title.
10. For some candidates, include career transitions or non-linear career paths.
11. Ensure career goals align with the candidate's experience and skills, but also show ambition and growth potential.
12. Make the projects section optional. focusing on candidates where project work would significantly enhance their profile.
"""

generated_resumes4=[
{
    "technical skills": "Java, Spring Boot, Microservices, AWS, Docker, Kubernetes, Agile",
    "experience": "- ABC Corp (FinTech, 500+ employees): Senior Software Engineer (2017 - Present)\n    - Led the development and deployment of a scalable microservices architecture on AWS.\n    - Mentored junior developers and conducted code reviews to ensure high-quality code.\n    - Contributed to the adoption of DevOps practices and CI/CD pipelines.",
    "education": "- Master of Science in Computer Science, University of Toronto (2017)\n- Bachelor of Engineering in Computer Engineering, University of Waterloo (2015)",

    "preferences": "Location: Toronto, Schedule: Full-time",

    "cultural_fit_indicators": "career_goal: Aspires to become a technical architect and lead large-scale software development projects. soft skills: Strong leadership skills, excellent communication, and a passion for mentoring and knowledge sharing. Overall Tone & presentation: Technical and results-oriented, showcasing expertise in Java development and cloud technologies."
},
{
    "technical skills": "Python, SQL, Data Analysis, Tableau, Power BI, Excel",
    "experience": "- DEF Corp (Healthcare, 1000+ employees): Data Analyst (2018 - Present)\n    - Conducted in-depth analysis of patient data to identify trends and improve healthcare outcomes.\n    - Developed interactive dashboards and reports to visualize key metrics and insights.\n    - Collaborated with clinical teams to implement data-driven initiatives.",
    "education": "- Bachelor of Science in Health Informatics, McMaster University (2018)",

    "preferences": "Location: Hamilton, Schedule: Full-time",

    "cultural_fit_indicators": "career_goal: Aspires to transition into a Data Scientist role and leverage machine learning expertise to make a positive impact in healthcare. soft skills: Analytical, detail-oriented, and passionate about improving patient care. Overall Tone & presentation: Data-focused and compassionate, showcasing a strong foundation in healthcare data analysis and a desire to drive positive change through data-driven solutions."
},
{
    "technical skills": "C#, .NET, ASP.NET, SQL, Agile, Git, Azure",
    "experience": "- GHI Corp (Software Development, 200+ employees): Software Engineer (2019 - Present)\n    - Developed and maintained web applications using C# and .NET on Azure.\n    - Collaborated with designers and product managers to implement new features and improve user experience.\n    - Contributed to the development of RESTful APIs for seamless communication between frontend and backend systems.",
    "projects": "- E-commerce Platform: Developed a full-stack e-commerce platform using C#, .NET, and Azure, handling product listings, shopping cart functionality, and payment processing.\n- Customer Relationship Management (CRM) System: Built a CRM system to manage customer interactions and track sales leads using C# and .NET.",
    "education": "- Bachelor of Computer Science, University of Victoria (2019)",

    "preferences": "Location: Victoria, Schedule: Full-time",

    "cultural_fit_indicators": "career_goal: Aims to become a senior .NET developer and contribute to building scalable and secure web applications. soft skills: Collaborative, problem-solver, and passionate about technology. Overall Tone & presentation: Technical and detail-oriented, showcasing a strong foundation in .NET development and a desire to create impactful web solutions."
},
{
    "technical skills": "JavaScript, React, Node.js, HTML, CSS, Git, Agile",
    "experience": "- JKL Corp (Tech Startup, 100+ employees): Front-End Developer (2017 - Present)\n    - Led the development of user interfaces for a high-traffic web application using React and JavaScript.\n    - Mentored junior developers and conducted code reviews to ensure code quality and maintainability.\n    - Implemented performance optimizations and responsive designs for various devices.",
    "education": "- Bachelor of Computer Science, University of New Brunswick (2017)",

    "preferences": "Location: Fredericton, Schedule: Full-time",

    "cultural_fit_indicators": "career_goal: Aspires to become a front-end architect and lead the development of complex user interfaces. soft skills: Strong leadership skills, excellent communication, and a passion for creating user-friendly experiences. Overall Tone & presentation: Technical and design-focused, showcasing expertise in front-end development and a commitment to delivering high-quality user interfaces."
},
{
    "technical skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, NLP, Computer Vision",
    "experience": "- MNO Corp (AI Research Lab, 20+ employees): Research Scientist (2021 - Present)\n    - Conducted research on computer vision and deep learning techniques for medical image analysis.\n    - Published research papers in top-tier conferences and journals.\n    - Collaborated with clinicians and researchers to develop and implement AI solutions for healthcare applications.",
    "education": "- PhD in Computer Science, University of Alberta (2021)\n- Master of Science in Computer Science, University of Calgary (2018)\n- Bachelor of Computer Science, University of Manitoba (2016)",

    "preferences": "Location: Edmonton, Schedule: Full-time",

    "cultural_fit_indicators": "career_goal: Aspires to continue conducting groundbreaking research in AI for healthcare and contribute to the development of innovative medical technologies. soft skills: Highly analytical, innovative thinker, and passionate about using AI to improve healthcare outcomes. Overall Tone & presentation: Academic and research-oriented, showcasing a deep understanding of AI and a commitment to making a positive impact in the healthcare field."
}
]
generated_resumes3=[
{
  "technical skills": "Python, Django, Flask, JavaScript, React, HTML, CSS, Git, Agile",
  "experience": "- IJK Corp (Tech Startup, 50+ employees): Full-Stack Developer (2018 - Present)\n    - Developed and maintained web applications using Python, Django, and React.\n    - Collaborated with designers and product managers to implement new features and improve user experience.\n    - Contributed to the development of RESTful APIs for seamless communication between frontend and backend systems.",
  "projects": "- E-commerce Platform: Developed a full-stack e-commerce platform using Python, Django, and React, handling product listings, shopping cart functionality, and payment processing.\n- Social Media Analytics Dashboard: Built a dashboard to visualize social media engagement metrics using Python, Flask, and JavaScript.",
  "education": "- Bachelor of Computer Science, University of Manitoba (2018)",

  "preferences": "Location: Winnipeg, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a senior full-stack developer and contribute to building innovative web applications. soft skills: Collaborative, problem-solver, and passionate about technology. Overall Tone & presentation: Technical and detail-oriented, showcasing a strong foundation in web development and a desire to create impactful user experiences."
},
{
  "technical skills": "Java, Spring, Hibernate, SQL, Agile, Git, Maven, Jenkins",
  "experience": "- LMN Corp (Financial Services, 1000+ employees): Software Engineer (2016 - 2020)\n    - Developed and maintained enterprise applications using Java, Spring, and Hibernate.\n    - Implemented database interactions using SQL and optimized queries for performance.\n    - Participated in code reviews and ensured adherence to coding standards and best practices.\n- OPQ Corp (Tech Consulting, 200+ employees): Software Engineer (2020 - Present)\n    - Designed and developed custom software solutions for clients across various industries.\n    - Collaborated with clients to gather requirements and translate them into technical specifications.\n    - Led a team of developers to deliver projects on time and within budget.",
  "education": "- Bachelor of Engineering in Software Engineering, McMaster University (2016)",

  "preferences": "Location: Hamilton, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to become a technical project manager and lead large-scale software development initiatives. soft skills: Strong leadership skills, excellent communication, and ability to manage complex projects. Overall Tone & presentation: Technical and results-oriented, showcasing expertise in Java development and project management."
},
{
  "technical skills": "Python, SQL, Data Analysis, Tableau, Power BI, Excel",
  "experience": "- RST Corp (Retail, 500+ employees): Data Analyst (2018 - Present)\n    - Analyzed sales data to identify trends, optimize pricing strategies, and improve inventory management.\n    - Developed interactive dashboards and reports to visualize key metrics and insights for business stakeholders.\n    - Collaborated with marketing and merchandising teams to implement data-driven initiatives for increasing sales and profitability.",
  "education": "- Bachelor of Commerce in Business Analytics, University of Alberta (2018)",

  "preferences": "Location: Edmonton, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Seeks to leverage data analysis skills to drive business growth and improve operational efficiency in the retail industry. soft skills: Analytical, results-oriented, and able to communicate effectively with cross-functional teams. Overall Tone & presentation: Data-focused and business-minded, showcasing a passion for using data to solve real-world retail challenges."
},
{
  "technical skills": "JavaScript, React, Node.js, HTML, CSS, Git, Agile",
  "experience": "- UVW Corp (Tech Startup, 30+ employees): Front-End Developer (2019 - Present)\n    - Developed and maintained user interfaces for web applications using React and JavaScript.\n    - Collaborated with designers to implement pixel-perfect designs and ensure a seamless user experience.\n    - Optimized front-end performance and implemented responsive designs for various devices.",
  "projects": "- Single-Page Application: Built a dynamic single-page application using React and Node.js, handling user authentication, data fetching, and real-time updates.\n- Interactive Data Visualization: Created interactive charts and graphs to visualize complex data sets using JavaScript and D3.js.",
  "education": "- Bachelor of Computer Science, University of Saskatchewan (2019)",

  "preferences": "Location: Saskatoon, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to become a senior front-end developer and contribute to building beautiful and user-friendly web applications. soft skills: Creative, detail-oriented, and passionate about user experience. Overall Tone & presentation: Technical and design-focused, showcasing a strong foundation in front-end development and a commitment to creating engaging user interfaces."
},
{
  "technical skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, NLP",
  "experience": "- XYZ Corp (Research Lab, 50+ employees): Research Scientist (2020 - Present)\n    - Conducted research on natural language processing and deep learning techniques.\n    - Published research papers in top-tier conferences and journals.\n    - Collaborated with other researchers to develop and implement cutting-edge AI algorithms.",
  "education": "- PhD in Computer Science, University of Toronto (2020)\n- Master of Science in Computer Science, University of Waterloo (2017)\n- Bachelor of Computer Science, University of British Columbia (2015)",

  "preferences": "Location: Toronto, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to continue conducting groundbreaking research in AI and contribute to the advancement of the field. soft skills: Highly analytical, innovative thinker, and effective communicator of complex ideas. Overall Tone & presentation: Academic and research-oriented, showcasing a deep understanding of AI and a passion for pushing the boundaries of knowledge."
}
]
generated_resumes2=[
{
  "technical skills": "Python, SQL, Data Analysis, Tableau, Power BI, Excel",
  "experience": "- QRS Corp (Healthcare, 500+ employees): Data Analyst (2019 - Present)\n    - Analyzed patient data to identify trends and improve healthcare outcomes.\n    - Developed dashboards and reports to visualize key metrics and insights.\n    - Collaborated with clinical teams to implement data-driven initiatives.",
  "education": "- Bachelor of Science in Health Informatics, University of Toronto (2019)",

  "preferences": "Location: Toronto, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to leverage data analysis skills to make a positive impact in the healthcare industry. soft skills: Analytical, detail-oriented, and passionate about improving patient care. Overall Tone & presentation: Data-focused and compassionate, showcasing a strong foundation in healthcare data analysis and a desire to drive positive change."
},
{
  "technical skills": "Java, Spring, Microservices, AWS, Docker, Kubernetes, Agile",
  "experience": "- TUV Corp (E-commerce, 1000+ employees): Software Engineer (2017 - Present)\n    - Designed, developed, and deployed scalable microservices using Java and Spring on AWS.\n    - Contributed to the development of a high-performance e-commerce platform.\n    - Implemented DevOps practices to streamline deployment and improve system reliability.",
  "education": "- Bachelor of Engineering in Software Engineering, University of Waterloo (2017)",

  "preferences": "Location: Kitchener-Waterloo, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a technical architect and lead complex software development projects. soft skills: Collaborative, problem-solver, and passionate about building scalable systems. Overall Tone & presentation: Technical and results-oriented, showcasing expertise in Java development and cloud technologies."
},
{
  "technical skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, NLP, Computer Vision",
  "experience": "- WXY Corp (AI Startup, 30+ employees): Machine Learning Engineer (2020 - Present)\n    - Developed and deployed machine learning models for natural language understanding and image recognition tasks.\n    - Contributed to research projects on cutting-edge AI techniques.\n    - Collaborated with cross-functional teams to implement AI solutions in real-world applications.",
  "projects": "- Chatbot Development: Built a conversational AI chatbot using deep learning and natural language processing techniques.\n- Object Detection for Autonomous Vehicles: Implemented a real-time object detection system for self-driving cars using computer vision and deep learning.",
  "education": "- Master of Science in Artificial Intelligence, University of Montreal (2020)\n- Bachelor of Computer Science, McGill University (2018)",

  "preferences": "Location: Montreal, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to become a leading AI researcher and contribute to the advancement of artificial intelligence. soft skills: Passionate about AI, quick learner, and thrives in a collaborative research environment. Overall Tone & presentation: Innovative and research-oriented, showcasing a strong foundation in AI and a desire to push the boundaries of machine learning."
},
{
  "technical skills": "R, Python, SQL, Data Analysis, Data Visualization, Statistics, Machine Learning",
  "experience": "- ZAB Corp (Market Research, 200+ employees): Data Scientist (2018 - Present)\n    - Conducted in-depth market research analysis using R and Python.\n    - Developed predictive models to forecast consumer behavior and market trends.\n    - Communicated findings and insights to clients through compelling visualizations and presentations.",
  "education": "- Master of Science in Statistics, University of British Columbia (2018)\n- Bachelor of Science in Mathematics, Simon Fraser University (2016)",

  "preferences": "Location: Vancouver, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a subject matter expert in applying data science to market research and consumer insights. soft skills: Analytical, detail-oriented, and able to translate complex data into actionable recommendations. Overall Tone & presentation: Data-driven and insightful, showcasing a passion for uncovering consumer trends and driving business growth."
},
{
  "technical skills": "SQL, Tableau, Power BI, Data Visualization, Data Analysis, Excel",
  "experience": "- CDE Corp (Non-Profit, 100+ employees): Data Analyst (2019 - Present)\n    - Analyzed fundraising and program data to measure impact and identify areas for improvement.\n    - Developed dashboards and reports to track key performance indicators and communicate results to stakeholders.\n    - Collaborated with program teams to implement data-driven strategies for maximizing social impact.",
  "education": "- Bachelor of Arts in Sociology, University of Calgary (2019)",

  "preferences": "Location: Calgary, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to use data analysis skills to drive positive social change and improve the lives of others. soft skills: Passionate about social impact, collaborative, and able to communicate effectively with diverse audiences. Overall Tone & presentation: Mission-driven and results-oriented, showcasing a strong foundation in data analysis and a commitment to making a difference."
},
{
  "technical skills": "C#, .NET, ASP.NET, SQL, Agile, Git, Azure",
  "experience": "- FGH Corp (Software Development, 500+ employees): Software Engineer (2016 - Present)\n    - Designed, developed, and maintained enterprise applications using C# and .NET on Azure.\n    - Contributed to the development of a scalable and secure cloud-based platform.\n    - Implemented best practices for code quality and performance optimization.",
  "education": "- Bachelor of Computer Science, Dalhousie University (2016)",

  "preferences": "Location: Halifax, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Seeks to become a technical lead and mentor junior developers in .NET technologies. soft skills: Collaborative, problem-solver, and committed to delivering high-quality code. Overall Tone & presentation: Technical and detail-oriented, showcasing expertise in C# development and cloud technologies."
}
]

generated_resumes1=[
{
  "technical skills": "Java, Spring Boot, Microservices, REST APIs, SQL, Agile, Git, Docker, Kubernetes",
  "experience": "- MNO Corp (Software Development, 500+ employees): Software Engineer (2016 - Present)\n    - Designed, developed, and maintained scalable and high-performance microservices using Java and Spring Boot.\n    - Implemented RESTful APIs for seamless communication between frontend and backend systems.\n    - Contributed to the adoption of DevOps practices, improving deployment frequency and reliability.",
  "education": "- Bachelor of Computer Science, University of Calgary (2016)",

  "preferences": "Location: Calgary, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to become a technical lead and mentor junior developers. soft skills: Collaborative, problem-solver, and eager to learn new technologies. Overall Tone & presentation: Technical and detail-oriented, demonstrating a passion for software development and a commitment to quality."
},
{
  "technical skills": "SQL, Tableau, Power BI, Data Visualization, Data Analysis, Excel, Python",
  "experience": "- PQR Corp (Retail, 1000+ employees): Data Analyst (2018 - Present)\n    - Conducted in-depth analysis of sales data to identify trends and opportunities for growth.\n    - Developed interactive dashboards and reports using Tableau and Power BI to visualize key metrics.\n    - Collaborated with business stakeholders to translate data insights into actionable recommendations.",
  "education": "- Bachelor of Commerce, University of Alberta (2018)",

  "preferences": "Location: Edmonton, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Seeks to leverage data analysis skills to drive business decisions and improve efficiency. soft skills: Strong analytical skills, excellent communication, and ability to work independently. Overall Tone & presentation: Data-focused and results-driven, demonstrating a passion for uncovering insights and driving positive change."
},
{
  "technical skills": "SQL, Data Warehousing, ETL, Business Intelligence, Data Modeling, Oracle, SAP",
  "experience": "- STU Corp (Manufacturing, 5000+ employees): Business Intelligence Analyst (2017 - Present)\n    - Designed and implemented data warehouses to support reporting and analytics needs.\n    - Developed ETL processes to extract, transform, and load data from various sources.\n    - Created and maintained reports and dashboards to track key performance indicators.",
  "education": "- Bachelor of Engineering, McMaster University (2017)",

  "preferences": "Location: Hamilton, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a subject matter expert in business intelligence and data warehousing. soft skills: Detail-oriented, problem-solver, and able to work effectively with technical and non-technical teams. Overall Tone & presentation: Analytical and organized, showcasing a passion for data and its application to business decision-making."
},
{
  "technical skills": "Google Ads, Search Engine Optimization (SEO), Pay-Per-Click (PPC), Google Analytics, Keyword Research, A/B Testing",
  "experience": "- VWX Corp (Digital Marketing Agency, 100+ employees): Paid Search Specialist (2019 - Present)\n    - Managed and optimized PPC campaigns across various industries, achieving significant improvements in ROI.\n    - Conducted keyword research and analysis to identify high-value search terms.\n    - Implemented A/B testing to optimize ad copy and landing pages for improved conversion rates.",
  "education": "- Bachelor of Marketing, Ryerson University (2019)",

  "preferences": "Location: Toronto, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to lead a paid search team and drive digital marketing success for clients. soft skills: Data-driven, results-oriented, and excellent communicator. Overall Tone & presentation: Marketing-savvy and analytical, demonstrating a passion for paid search and a focus on achieving measurable results."
},
{
  "technical skills": "Facebook Ads, Instagram Ads, Social Media Marketing, Content Creation, Audience Targeting, Performance Analysis",
  "experience": "- YZA Corp (E-commerce, 500+ employees): Paid Social Specialist (2018 - Present)\n    - Planned, executed, and optimized social media advertising campaigns across Facebook and Instagram.\n    - Developed engaging ad creatives and targeted audience segments to maximize reach and engagement.\n    - Analyzed campaign performance data to identify areas for improvement and optimize ad spend.",
  "education": "- Bachelor of Arts in Communications, Concordia University (2018)",

  "preferences": "Location: Montreal, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a social media marketing expert and drive brand awareness and customer acquisition through paid social channels. soft skills: Creative, data-driven, and passionate about social media. Overall Tone & presentation: Engaging and results-oriented, showcasing a strong understanding of social media advertising and a focus on achieving business objectives."
},
{
  "technical skills": "Google Ads, Facebook Ads, Programmatic Advertising, Display Advertising, Media Buying, Campaign Management",
  "experience": "- BCD Corp (Media Agency, 200+ employees): Paid Media Specialist (2017 - Present)\n    - Planned and executed integrated paid media campaigns across various channels, including search, social, and display.\n    - Negotiated media buys and managed ad placements to maximize reach and efficiency.\n    - Tracked and analyzed campaign performance to optimize budget allocation and achieve client goals.",
  "education": "- Bachelor of Business Administration, University of Victoria (2017)",

  "preferences": "Location: Victoria, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Seeks to become a strategic media planner and drive successful paid media campaigns for clients. soft skills: Analytical, detail-oriented, and able to manage multiple projects simultaneously. Overall Tone & presentation: Results-driven and organized, demonstrating a passion for paid media and a focus on achieving client objectives."
},
{
  "technical skills": "Python, SQL, Data Analysis, Data Visualization, Machine Learning, Statistics",
  "experience": "- EFG Corp (Consulting, 100+ employees): Data Analyst (2020 - Present)\n    - Conducted data analysis and visualization to support client projects across various industries.\n    - Developed and implemented machine learning models to solve business problems and improve decision-making.\n    - Communicated findings and insights to clients through clear and concise presentations.",
  "education": "- Master of Science in Analytics, University of Ottawa (2020)\n- Bachelor of Science in Statistics, Carleton University (2018)",

  "preferences": "Location: Ottawa, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to transition into a Data Scientist role and leverage machine learning expertise to solve complex problems. soft skills: Analytical, problem-solver, and able to work effectively in a team environment. Overall Tone & presentation: Data-driven and results-oriented, showcasing a strong foundation in analytics and a desire to apply machine learning to real-world challenges."
},
{
  "technical skills": "Python, Django, Flask, JavaScript, React, HTML, CSS, Git, Agile",
  "experience": "- HIJ Corp (Tech Startup, 50+ employees): Software Engineer (2019 - Present)\n    - Developed and maintained web applications using Python, Django, and React.\n    - Collaborated with designers and product managers to implement new features and improve user experience.\n    - Contributed to the development of RESTful APIs for seamless communication between frontend and backend systems.",
  "projects": "- E-commerce Platform: Developed a full-stack e-commerce platform using Python, Django, and React, handling product listings, shopping cart functionality, and payment processing.\n- Social Media Analytics Dashboard: Built a dashboard to visualize social media engagement metrics using Python, Flask, and JavaScript.",
  "education": "- Bachelor of Computer Science, University of Manitoba (2019)",

  "preferences": "Location: Winnipeg, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a full-stack developer and contribute to building innovative web applications. soft skills: Collaborative, problem-solver, and passionate about technology. Overall Tone & presentation: Technical and detail-oriented, showcasing a strong foundation in web development and a desire to create impactful user experiences."
},]
generated_resumes=[
  {
  "technical skills": "Python, SQL, Apache Spark, Hadoop, AWS, ETL, Data Warehousing, Data Modeling, Airflow, Kafka",
  "experience": " - ABC Corp (E-commerce, 10,000+ employees): Senior Data Engineer (2018 - Present)\n    - Designed and implemented a scalable data pipeline using Apache Spark on AWS, reducing data processing time by 40%.\n    - Developed and maintained data warehouses for business intelligence and analytics, improving query performance by 30%.\n    - Collaborated with cross-functional teams to gather data requirements and translate them into technical solutions.\n - XYZ Inc (FinTech, 500+ employees): Data Engineer (2015 - 2018)\n    - Built and optimized ETL processes to extract, transform, and load data from various sources into a centralized data lake.\n    - Implemented data quality checks and monitoring to ensure data accuracy and integrity.\n    - Contributed to the development of a real-time data streaming platform using Kafka.",
  "education": "- Master of Science in Computer Science, University of Toronto (2015)\n- Bachelor of Engineering in Computer Engineering, University of Waterloo (2013)",

  "preferences": "Location: Toronto, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to lead a data engineering team and contribute to building innovative data-driven solutions. soft skills: Strong problem-solver, collaborative team player, and effective communicator. Overall Tone & presentation: Professional and results-oriented, showcasing technical expertise and a passion for data."
  },
  {
  "technical skills": "Python, R, Machine Learning, Deep Learning, Data Visualization, SQL, Statistics, TensorFlow, PyTorch, Scikit-learn",
  "experience": "- DEF Corp (Healthcare, 1000+ employees): Data Scientist (2017 - Present)\n    - Developed and deployed machine learning models for patient risk prediction, improving accuracy by 20%.\n    - Conducted exploratory data analysis to identify trends and insights for clinical decision support.\n    - Collaborated with clinicians and researchers to design and implement data-driven solutions.\n - GHI Inc (Consulting, 50+ employees): Data Analyst (2015 - 2017)\n    - Performed data cleaning, preparation, and analysis for various client projects.\n    - Created interactive dashboards and visualizations to communicate findings to stakeholders.\n    - Assisted in developing data-driven recommendations for clients.",

  "education": "- Master of Science in Data Science, University of British Columbia (2017)\n- Bachelor of Science in Mathematics, Simon Fraser University (2015)",

  "preferences": "Location: Vancouver, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a subject matter expert in applying data science to healthcare challenges. soft skills: Analytical thinker, detail-oriented, and able to bridge the gap between technical and non-technical audiences. Overall Tone & presentation: Data-driven and insightful, demonstrating a passion for using data to solve real-world problems."
},
{
  "technical skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, NLP, Computer Vision",
  "experience": "- JKL Corp (AI Startup, 20+ employees): Machine Learning Intern (2022 - 2023)\n    - Assisted in developing and training deep learning models for natural language processing tasks.\n    - Implemented and evaluated various machine learning algorithms for image classification.\n    - Contributed to research projects on cutting-edge machine learning techniques.",
  "projects": "- Sentiment Analysis on Social Media Data: Developed a machine learning model to classify sentiments in social media posts, achieving an accuracy of 85%.\n- Image Recognition for Autonomous Vehicles: Implemented a convolutional neural network to detect objects in images for self-driving cars.",
  "education": "- Bachelor of Computer Science, McGill University (2023)\n- Relevant coursework: Machine Learning, Deep Learning, Artificial Intelligence.",

  "preferences": "Location: Montreal, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Eager to learn and grow as a machine learning engineer, contributing to the development of innovative AI applications. soft skills: Quick learner, passionate about technology, and thrives in a fast-paced environment. Overall Tone & presentation: Enthusiastic and motivated, showcasing a strong foundation in machine learning and a desire to make an impact."
},{
  "technical skills": "Java, Spring Boot, Microservices, REST APIs, AWS, Docker, Kubernetes, Agile, Git",
  "experience": "- MNO Corp (Energy, 5000+ employees): Senior Software Engineer (2016 - Present)\n    - Led the development of a cloud-native microservices architecture using Spring Boot and AWS, improving system scalability and resilience.\n    - Designed and implemented REST APIs for seamless integration between various services.\n    - Mentored junior developers and fostered a culture of collaboration and continuous learning.\n - PQR Inc (Software Consulting, 100+ employees): Software Engineer (2013 - 2016)\n    - Developed and maintained enterprise Java applications for clients across various industries.\n    - Contributed to the full software development lifecycle, from requirements gathering to deployment and maintenance.\n    - Worked closely with clients to understand their needs and deliver high-quality solutions.",
  "education": "- Bachelor of Science in Computer Science, University of Calgary (2013)",

  "preferences": "Location: Calgary, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aspires to become a technical lead and guide teams in building robust and scalable software systems. soft skills: Strong problem-solver, collaborative team player, and effective communicator. Overall Tone & presentation: Professional and results-oriented, showcasing technical expertise and a passion for software development."
},
{
  "technical skills": "SQL, Excel, Tableau, Power BI, Data Visualization, Data Cleaning, Data Analysis",
  "experience": "- STU Corp (Retail, 1000+ employees): Data Analyst (2018 - Present)\n    - Conducted in-depth sales analysis to identify trends and opportunities for growth.\n    - Created interactive dashboards and reports to track key performance indicators and provide actionable insights.\n    - Collaborated with marketing and merchandising teams to optimize pricing and promotions.\n - VWX Inc (Non-Profit, 50+ employees): Data Analyst Intern (2017)\n    - Assisted in collecting, cleaning, and analyzing data on program effectiveness.\n    - Created visualizations to communicate findings to stakeholders and donors.",
  "education": "- Bachelor of Commerce, University of Alberta (2018)\n- Major: Business Analytics",

  "preferences": "Location: Edmonton, Schedule: Full-time",

  "cultural_fit_indicators": "career_goal: Aims to become a data analytics expert, driving data-informed decision-making across the organization. soft skills: Analytical thinker, detail-oriented, and able to communicate complex data insights in a clear and concise manner. Overall Tone & presentation: Data-driven and results-oriented, showcasing a passion for uncovering insights from data and translating them into actionable recommendations."
},

]
