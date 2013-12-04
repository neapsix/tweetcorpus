import nltk

sentences = []

def process_texts(text_list):
    #input a list of strings
    for t in text_list:
        #normally we would use
        #tokens = nltk.word_tokenize(t)
        #but tweets are harder to parse, so we need some more robust rules

        #set up regex rules for the tokenizer
        sentence_re = r'''(?x)  # set flag to allow verbose regexps
            ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
            | (https?://[^ ]+)      # websites--we do this upstream of words because otherwise words captures 'http'
            | \w+(-\w+)*            # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
            | \#?\w+|\@?\w+         # hashtags and @ signs
            | \.\.\.                # ellipsis
            | [][.,;"'?()-_`]       # these are separate tokens
            #| http://t.co/[a-z,A-Z,0-9]{10} # twitter urls?
            '''
        
        #separate each string into tokens
        tokens = nltk.regexp_tokenize(t, sentence_re)

        #make a text for each tokenized string
        new_text = nltk.Text(tokens)

        #modify tagger to tag hashtags and @signs as different parts of speech
        #maybe @signs are just proper nouns--unsure about this, but can change it later
        #should we maybe also tag urls as a part of speech?
        default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
        model = [('\#\w+','HT'), ('\@\w+','AT')]
        tagger = nltk.RegexpTagger(model, backoff=default_tagger)

        print(tagger.tag(new_text))
        
        #drop each new text in a list
        sentences.append(new_text)


sample = ['@zabraham10 for ??',
    'ITS TOO EARLY FOR THIS ASDFGKVLDLDo http://t.co/8Q9QlDvUoQ',
    'its just can my one up just can so me my when find u not your I',
    '-Mnager of number eight basically laughed in my face when I asked about the job in there hahaha cheers',
    'I\'m not even pooping omg I https://t.co/8Q9QlDvUoQ',
    'Mexican cheese dip & Doritos = good eating',
    '2 down 1 to go',
    'RT @_RyanHowell: Imagine what a rainbow would taste like....',
    '@VCrippen this should be a broadway musical! #lol #waffles']

process_texts(sample)
print(sentences[0])
print(sentences[1])
print(sentences[-1:])
