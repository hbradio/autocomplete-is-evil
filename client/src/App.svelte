<script>
  import { onMount, tick } from "svelte";
  import { fade } from "svelte/transition";
  import { debounce } from "throttle-debounce";

  export let path;

  let completion = "";
  let phrase = "Dear ";
  let showCopySuccess = false;
  let showModelInfo = false;
  let showQA = false;
  let firstAutocompleteDone = false;
  let inputElement;

  const models = [
    {
      label: "Model A",
      id: "shakespeare001",
      description: "the entire text of Shakespeare's play Hamlet",
      link: "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt",
    },
    {
      label: "Model B",
      id: "trumptweets001",
      description: "all tweets from @realdonaldtrump through January 8th, 2021",
      link: "https://www.thetrumparchive.com/",
    },
    {
      label: "Model C",
      id: "dccc001",
      description:
        "all emails to the supporter mailing list of the Democratic Contressional Comapign Committee, 2019-06-27 to 2021-11-15",
      link: "https://politicalemails.org/organizations/662",
    },
    {
      label: "Model D",
      id: "gopaz001",
      description:
        "emails to the supporter mailing list of the Republican party of Arizona, 2019-07-24 to 2021-11-14",
      link: "https://politicalemails.org/organizations/826",
    },
    {
      label: "Model E",
      id: "kjv001",
      description:
        "the King James Version of the Bible, both Old and New Testaments",
      link: "https://www.gutenberg.org/ebooks/10",
    },
  ];

  let model = models[0];
  $: model, (showModelInfo = false);

  const handleTyping = (event) => {
    const key = event.keyCode || event.charCode;
    if (key == 13) {
      event.preventDefault();
      acceptCompletion();
      return;
    }
    if (key < 48 || key > 90) {
      // Not a-z0-9
      return;
    }
    completion = "";
    fetchCompletion();
  };

  async function acceptCompletion() {
    phrase = phrase + completion;
    completion = "";
    await tick();
    setCursor();
  }

  const fetchCompletion = debounce(1500, () => {
    completion = "...";
    const uriPhrase = encodeURI(phrase);
    fetch(
      `https://nedk6qxpi5.execute-api.us-east-1.amazonaws.com/deployed/completion?type=${model.id}&phrase=${uriPhrase}`
    )
      .then((response) => response.json())
      .then((data) => {
        completion = data.completion;
        if (firstAutocompleteDone == false) {
          setTimeout(() => (firstAutocompleteDone = true), 5000);
        }
      });
  });

  function setCursor() {
    let range, selection;
    range = document.createRange(); // Create a range (a range is a like the selection but invisible)
    range.selectNodeContents(inputElement); // Select the entire contents of the element with the range
    range.collapse(false); // Collapse the range to the end point. false means collapse to end rather than the start
    selection = window.getSelection(); // Get the selection object (allows you to change selection)
    selection.removeAllRanges(); // Remove any selections already made
    selection.addRange(range); // Make the range you have just created the visible selection
  }

  function copyText() {
    const text = phrase + completion;
    navigator.clipboard.writeText(text).then(
      () => {
        console.log("Copying to clipboard was successful! Woo!");
        showCopySuccess = true;
        console.log(showCopySuccess);
        setTimeout(() => (showCopySuccess = false), 3000);
      },
      (err) => alert("Sorry, could not copy to clipboard.")
    );
  }

  onMount(() => {
    setCursor();
  });
</script>

<main>
  <header>
    <h1>Autocomplete Playground</h1>
  </header>
  <div class="flex-container">
    <section class="composing-column">
      <label for="model"><h3>Choose an autocomplete model.</h3></label>
      <select bind:value={model} name="model" id="model">
        {#each models as m}
          <option value={m}>{m.label}</option>
        {/each}
      </select>
      <h3>
        Compose an email to a friend in the box below.
      </h3>
      <p>Press <em>enter</em> to accept suggestions.</p>
      <div class="email-area">
        <div class="dummy-input"><em>To: </em>my.friend@gmail.com</div>
        <div class="dummy-input"><em>Subject: </em>Hey, how's it going?</div>
        <div class="composing-area" on:click={setCursor} style="margin-bottom: -50px;">
          <span
            bind:this={inputElement}
            contenteditable="true"
            bind:innerHTML={phrase}
            class="input-block"
            on:click|stopPropagation
            on:keydown={handleTyping}
          />
          {#if completion !== ""}
            <spon class="completion-text">{completion} ⏎</spon>
          {/if}
        </div>
      </div>
      <button on:click={copyText} style="padding: 10px; position:relative; top: -20px; left: 10px">
        {#if !showCopySuccess}
          <i class="gg-copy" />
        {/if}
        {#if showCopySuccess}
          <i class="gg-check" />
        {/if}
      </button>
    </section>

    <section class="info-column">
      {#if firstAutocompleteDone}
        <div transition:fade>
          <h3>
            What do the autocomplete suggestions sound like to you?
          </h3>
          <p>Can you guess what source text the model was trained on?</p>
          {#if !showModelInfo}
            <button on:click={() => (showModelInfo = true)}>Show me</button>
          {/if}
          {#if showModelInfo}
            <button on:click={() => (showModelInfo = false)}>Hide info</button
            >
          {/if}
          {#if showModelInfo}
            <div transition:fade>
              <p>
                Autocomplete <em>{model.label}</em> was generated from
                <a href={model.link}>{model.description}</a>.
              </p>
            </div>
          {/if}
        </div>
      {/if}
    </section>
  </div>
  {#if firstAutocompleteDone}
    <section transition:fade style="text-align:center">
      <h2>What is all this?</h2>
      {#if !showQA}
        <button on:click={() => (showQA = true)}>Show Q&A</button>
      {/if}
      {#if showQA}
        <button on:click={() => (showQA = false)}>Hide Q&A</button>
      {/if}
      {#if showQA}
        <div transition:fade class="qa">
          <h3>What's your point here?</h3>
          <p>I think text autocomplete is low-grade mind control.</p>
          <h3>Mind control? Isn't that a little dramatic?</h3>
          <p>
            Gmail <a
              href="https://www.blog.google/products/gmail/subject-write-emails-faster-smart-compose-gmail/"
            >
              suddenly starting finishing the thoughts</a
            >
            of its
            <a
              href="https://www.cnbc.com/2019/10/26/gmail-dominates-consumer-email-with-1point5-billion-users.html"
            >
              1.5 billion users</a
            >. It's hard to be hyperbolic when talking about something running at
            that scale.
          </p>
          <h3>
            But Google says that Gmail's suggestions personalized to me. Aren't
            they based on what I've written in the past?
          </h3>
          <p>Would you know if they weren't?</p>
          <h3>
            But creating an autocomplete model requires special expertise and
            careful use of advanced technology, right?
          </h3>
          <p>
            Not really. I've studied machine learning, but I'm not a deep learning
            guru. I made these autocomplete models by copying <a
              href="https://colab.research.google.com/github/yashk2810/tensorflow/blob/005799649aae3fe4a01a8e69cf88ebbcd86ca8f0/tensorflow/contrib/eager/python/examples/generative_examples/text_generation.ipynb"
            >
              a recursive neural network tutorial from Google.</a
            >
            using a pretty standard gaming PC.
            <a
              href="https://www.technologyreview.com/2020/07/20/1005454/openai-machine-learning-language-generator-gpt-3-nlp/"
              >The really advanced stuff</a
            > is much more powerful.
          </p>
          <h3>What should I do?</h3>
          <p>
            <a
              href="https://support.google.com/mail/answer/9116836?hl=en&co=GENIE.Platform%3DDesktop"
              >Turn off Smart Compose in Gmail</a
            >. Think your own thoughts.
          </p>
          <h3>Can we chat?</h3>
          <p>Sure! Email me: brady.hurlburt [at] pm.me</p>
          <h3>Can I see the code?</h3>
          <p>
            <a href="https://github.com/hbradio/autocomplete-is-evil">Sure!</a>
          </p>
        </div>
      {/if}
    </section>
  {/if}
</main>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Balsamiq+Sans:wght@700&family=Roboto&display=swap');
  main {
    font-family: 'Roboto', sans-serif;
    max-width: 1400px;
    margin: 0 auto;
    padding-bottom: 100px;
  }

  p {
    margin-top: 0.4em;
    line-height: 1.5em;
  }

  h1, h2, h3 {
    font-family: 'Balsamiq Sans', cursive;
    margin-top: 0.6em;
    margin-bottom: 0.2em;
  }

  h3 {
    font-size: 1.6em;
    margin-bottom: 0.1em;
  }

  h2 {
    font-size: 3.0em;
  }

  h1 {
    font-size: 3.8em;
    text-shadow: -10px 10px 0px #e7e7e755,
                 -20px 20px 0px #c0c0c055,
                 -30px 30px 0px #9b9b9b55;
  }

  header {
    text-align: center;
    margin-bottom: 1em;
  }

  button, select {
    font-size: 1.2em;
  }

  section {
    margin: 0.5em 2em;
  }

  .flex-container {
    display: flex;
    flex-direction: row;
  }

  .composing-column {
    flex: 2;
  }

  .info-column {
    flex: 1;
  }

  @media (max-width: 900px) {
    .flex-container {
      flex-direction: column;
    }
  }

  .email-area {
    box-shadow: 10px 10px 8px grey;
  }

  .dummy-input {
    border-style: solid;
    border-color: grey;
    padding: 0.5rem 0.5rem 0.5rem 0.5rem;
    background-color: white;
  }

  .composing-area {
    border-style: solid;
    border-color: grey;
    padding: 1rem 0.5rem 1.5rem 0.5rem;
    min-height: 200px;
    background-color: white;
  }

  .input-block {
    padding: 0 0.5rem 0 0;
    outline-style: none;
  }

  .completion-text {
    background-color: #f19f4d5d;
  }

  .qa {
    text-align: left;
    margin: 0 auto;
    max-width: 700px;
  }
</style>
