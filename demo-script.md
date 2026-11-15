# Three-minute judging video

**Team Solon Superintelligence · Sleep on It**

Aim for 155–160 words per minute while speaking. The timestamps and slide cues are for the recording. Use the left and right arrow keys to advance. Let each chart start drawing as you reach its slide. Hold the final frame through 3:00 and export as an MP4 under 500 MB.

### 0:00 · Slide 1 · Title

Can a dataset get the average right and still teach a model the wrong thing? We’re Team Solon Superintelligence. For the Sleep on It challenge, we put the provided sleep dataset to that test.

### 0:14 · Slide 2 · Kaggle acknowledgement

The creator says the records were made for illustration. We wanted to see which patterns would hold up against data from real people.

### 0:23 · Slide 3 · The two datasets

We used all three hundred seventy-four synthetic records. In Python, we joined six kinds of CDC survey files by participant ID. Then we kept employed adults in the same age range with valid sleep answers. That gave us four thousand four hundred twenty-three participants.

### 0:41 · Slide 4 · Averages

At first, the averages look close. Seven point one versus six point seven hours of sleep. And about four in ten in both files sleep under seven hours. So what happens when we compare relationships?

### 0:55 · Slide 5 · Correlations

Each pair of dots shows the same correlation in the two files. Look at pulse and sleep. The blue dot is at minus point five two. The gray dot is near zero. A model could learn a relationship that barely appears in this survey.

### 1:13 · Slide 6 · BMI composition

Then we checked who was represented. Only three percent of synthetic records fell in the obesity category, compared with thirty-seven percent in the survey. Similar averages can hide how differently groups are represented.

### 1:26 · Slide 7 · Short sleep by BMI

We tried comparing sleep problems, but the files capture different things. One labels disorders and the other asks about sleep trouble. We switched to sleeping under seven hours. In the overweight group, that’s seventy-six percent synthetic versus forty-two percent real.

### 1:43 · Slide 8 · Activity and sleep

Both lines slope down. Short sleep was less common in the higher-activity group in each file. The synthetic file tracks daily activity. The survey records weekly leisure activity. Those lines can’t tell us how much exercise changes sleep.

### 1:59 · Slide 9 · Variability

The synthetic file also compresses the range of sleep. Every value is between five point eight and eight point five hours. The survey spans a wider range.

### 2:10 · Slide 10 · Why it matters

A team testing a model on synthetic health records could do the same check before relying on it. Compare who’s represented, how much the values vary, and which variables move together.

### 2:23 · Slide 11 · Data and methods

The app shows how we defined each measure and how many records went into it. A Python script rebuilds the figures, and the presentation runs from a single offline HTML file.

### 2:36 · Slide 12 · Duplicate check

We also removed exact copies, ignoring the ID. That left one hundred thirty-two distinct rows. The pulse correlation barely moved, to minus point five one. Next we’d repeat the comparison using a newer survey and survey weights.

### 2:52 · Slide 13 · Thank you

Before relying on synthetic data, check whether the patterns it could teach a model show up in real data.
