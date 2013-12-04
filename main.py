import nltk

corpus = {}

def make_corpus(text_list):
    corpus['words'] = []
    corpus['tagged_words'] = []
    corpus['sents'] = []
    corpus['tagged_sents'] = []
    #input a list of strings
    for t in text_list:
        #set up regex rules that the tokenizer will use to parse strings
        token_pattern = r'''(?x)  # allow verbose regex
            ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A. - upstream of words
            | (https?://[^ ]+)      # URLs - do this upstream of words because otherwise words will capture 'http'
            | \w+(-\w+)*            # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?      # currency and percentages
            | \#?\w+|\@?\w+         # hashtags and @signs
            | \.\.\.                # ellipsis
            | [][.,;"'?()-_`]       # these are separate tokens
            #| http://t.co/[a-z,A-Z,0-9]{10} # twitter URLs - the URL pattern above gets them just fine
            '''
        
        #parse each string into tokens
        tokens = nltk.regexp_tokenize(t, token_pattern)
        
        #merge these into the total list of words
        corpus['words'] += tokens

        #make a text (sentence) for each tokenized string 
        #should I use the Text object, or a list of tokens?
        #new_text = nltk.Text(tokens)
        new_text = tokens

        #append the new text to the list of sentences
        corpus['sents'].append(new_text)

        #modify tagger to tag hashtags and @signs as different parts of speech
        #maybe @signs are just proper nouns--unsure about this, but can change it later
        #should we maybe also tag urls as a part of speech? 
        #how about emoticons (hard to parse them, but could grab one or two specific ones)?
        default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
        model = [('\#\w+','HT'), ('\@\w+','AT')]
        tagger = nltk.RegexpTagger(model, backoff=default_tagger)
        
        #tag the tokens with part of speech
        tagged_tokens = tagger.tag(tokens)

        #merge these into the total list of tagged words
        corpus['tagged_words'] += tagged_tokens
        
        #make a text for the tagged, tokenized strings
        new_tagged_text = tagged_tokens

        #append the new tagged text to the list of tagged sentences
        corpus['tagged_sents'].append(new_tagged_text)


sample = ['@zabraham10 for ??',
    'ITS TOO EARLY FOR THIS ASDFGKVLDLDo http://t.co/8Q9QlDvUoQ',
    'its just can my one up just can so me my when find u not your I',
    '-Mnager of number eight basically laughed in my face when I asked about the job in there hahaha cheers',
    'I\'m not even pooping omg I https://t.co/8Q9QlDvUoQ',
    'Mexican cheese dip & Doritos = good eating',
    '2 down 1 to go',
    'RT @_RyanHowell: Imagine what a rainbow would taste like....',
    '@VCrippen this should be a broadway musical! #lol #waffles']

make_corpus(sample)

print(corpus['words'])

