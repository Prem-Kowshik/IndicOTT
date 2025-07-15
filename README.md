# IndicOTT - Multilingual Indian Cinema Streaming Platform

![StreamFlix Logo](https://img.shields.io/badge/StreamFlix-🎬-red) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-brightgreen) ![License](https://img.shields.io/badge/License-MIT-green)

**IndicOTT** is a comprehensive multilingual streaming platform designed specifically for Indian cinema and public domain films. Built with Streamlit, it provides a Netflix-like experience with extensive language support, AI-powered movie analysis, and seamless video playback capabilities.

## 🌟 Features

### 🎬 Video Streaming
- **High-quality video playback** with WebM and OGV format support
- **Responsive video player** with subtitle integration
- **Carousel-style homepage** featuring curated movie collections
- **Grid-based movie browsing** with detailed metadata
- **Video statistics tracking** (duration, file size, resolution)

### 🌐 Multilingual Support
- **12+ Indian languages** including Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Punjabi, Kannada, Malayalam, Urdu, and Nepali
- **Real-time language switching** with cached translations
- **On-screen keyboard support** for Indian scripts
- **Subtitle support** in multiple languages with VTT format
- **Localized UI elements** for better user experience

### 🤖 AI-Powered Features
- **Movie Trope Analysis** using Google Gemini AI
- **Character archetype identification** and analysis
- **Thematic element extraction** from film content
- **Automated movie metadata generation**
- **Confidence scoring** for AI-generated insights

### 📱 User Interface
- **Modern Netflix-inspired design** with dark theme
- **Responsive layout** optimized for various screen sizes
- **Interactive search functionality** with real-time filtering
- **Customizable viewing preferences** per user
- **Seamless navigation** between sections

### 🗄️ Data Management
- **Supabase integration** for scalable data storage
- **Cached translation system** for instant language switching
- **Genre-based categorization** and filtering
- **Director and cast-based browsing**
- **Year-wise movie classification**

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip package manager
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Prem-Kowshik/IndicOTT.git
cd IndicOTT
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.streamlit/secrets.toml` file:
```toml
[supabase]
url = "your_supabase_url"
key = "your_supabase_anon_key"
```

4. **Generate translations (optional)**
```bash
python generate_translations.py
```

5. **Run the application**
```bash
streamlit run Homepage.py
```

## 📁 Project Structure

```
IndicOTT/
├── Homepage.py                 # Main application entry point
├── requirements.txt           # Python dependencies
├── generate_translations.py   # Translation generation script
├── response_testing.py        # Database connection testing
├── testing.py                 # Data classification functions
├── genre_utils.py             # Genre-related utilities
├── translations_cache.json    # Cached translations
├── CHANGELOG                  # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── .streamlit/
│   └── secrets.toml          # Configuration secrets
├── pages/
│   ├── 01_Video_Player.py    # Video playback interface
│   ├── 04_Index.py           # Movie database browser
│   └── 05_Feedback.py        # User feedback form
└── utils/
    ├── ai_utils.py           # AI analysis functions
    ├── supabase_client.py    # Database client
    ├── translation_utils.py  # Translation management
    └── keyboard_component.py # On-screen keyboard
```

## 🔧 Configuration

### Database Setup
The application uses Supabase for data storage. Required tables:
- `Movies_with_embedded_video` - Video metadata
- `Video_movies` - Movie information
- `subtitles` - Subtitle data
- `Genre Data` - Genre classifications

### API Keys
Configure the following in your secrets file:
- **Supabase URL and Key** - Database access
- **Google Gemini API Key** - AI analysis features

### Translation Cache
Generate translations using:
```bash
python generate_translations.py
```

## 🎯 Usage

### Basic Navigation
1. **Homepage** - Browse featured movies and search content
2. **Video Player** - Watch movies with subtitle support
3. **Movie Index** - Browse complete movie database
4. **Feedback** - Submit user feedback

### Language Selection
- Choose your preferred language from the dropdown
- All UI elements will update in real-time
- Subtitle preferences are saved per session

### Video Playback
- Click "Watch" on any movie to start playback
- Use the subtitle selector to change languages
- Download subtitles in SRT format

### AI Analysis
- Click "Analyze Tropes" in the video player
- Get detailed character and thematic analysis
- View confidence scores for AI insights

## 🛠️ Development

### Code Structure
- **Frontend**: Streamlit-based reactive UI
- **Backend**: Supabase for data persistence
- **AI Integration**: Google Gemini for content analysis
- **Multilingual**: JSON-based translation system

### Key Technologies
- **Streamlit 1.45.1** - Web application framework
- **Supabase** - Backend-as-a-Service
- **Google Generative AI** - Movie analysis
- **OpenCV** - Video processing
- **Pandas** - Data manipulation

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📊 Features in Detail

### Video Streaming Architecture
- **Format Support**: WebM (VP9/VP8), OGV (Theora)
- **Quality Options**: HD, 4K support where available
- **Adaptive Streaming**: Automatic quality adjustment
- **Subtitle Integration**: VTT format with timing support

### AI Analysis System
The AI system provides:
- **Character Archetype Analysis** - Identifies common character types
- **Narrative Pattern Recognition** - Detects storytelling conventions
- **Thematic Element Extraction** - Identifies key themes
- **Historical Context Analysis** - Provides cultural significance
- **Confidence Scoring** - Reliability metrics for insights

### Language Support Matrix
| Language | UI Support | Subtitles | Keyboard |
|----------|------------|-----------|----------|
| English  | ✅ | ✅ | ✅ |
| Hindi    | ✅ | ✅ | ✅ |
| Bengali  | ✅ | ✅ | ✅ |
| Tamil    | ✅ | ✅ | ✅ |
| Telugu   | ✅ | ✅ | ✅ |
| Marathi  | ✅ | ✅ | ❌ |
| Gujarati | ✅ | ✅ | ❌ |
| Punjabi  | ✅ | ✅ | ❌ |
| Kannada  | ✅ | ✅ | ❌ |
| Malayalam| ✅ | ✅ | ❌ |
| Urdu     | ✅ | ✅ | ❌ |
| Nepali   | ✅ | ✅ | ❌ |

## 🔍 Data Sources

### Primary Content
- **Wikimedia Commons** - Public domain video content
- **Internet Archive** - Historical film collections
- **Cultural Heritage** - Preserved cinema collections

### Metadata Sources
- **Manual Curation** - Director, cast, genre information
- **AI Enhancement** - Automated analysis and tagging
- **Community Input** - User-generated content and feedback

## 🐛 Troubleshooting

### Common Issues
1. **Video won't play** - Check internet connection and browser compatibility
2. **Subtitles not loading** - Ensure language is available in database
3. **AI analysis fails** - Verify Google Gemini API key configuration
4. **Translation errors** - Regenerate translation cache

### Performance Optimization
- **Caching**: Translations are cached for instant access
- **Lazy Loading**: Content loads on-demand
- **Compression**: Video files are optimized for streaming
- **CDN**: Static assets served from optimized locations

## 📈 Roadmap

### Upcoming Features
- [ ] **Offline Viewing** - Download movies for offline access
- [ ] **User Profiles** - Personal watchlists and preferences
- [ ] **Recommendation Engine** - AI-powered movie suggestions
- [ ] **Social Features** - Ratings, reviews, and sharing
- [ ] **Advanced Search** - Faceted search with multiple filters
- [ ] **Mobile App** - Native mobile applications

### Long-term Vision
- **Regional Expansion** - Support for more Indian languages
- **Content Partnerships** - Collaborations with content creators
- **Educational Integration** - Learning resources and cultural context
- **Community Platform** - User-generated content and discussions

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Pull request process
- Issue reporting
- Feature requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- **Wikimedia Commons** - For providing public domain video content
- **Google Generative AI** - For powering our AI analysis features
- **Supabase** - For reliable backend infrastructure
- **Streamlit** - For the excellent web application framework
- **Contributors** - Everyone who has contributed to this project

## 📞 Support

For support, please:
1. Check the [Issues](https://github.com/Prem-Kowshik/IndicOTT/issues) page
2. Create a new issue if needed
3. Use the in-app feedback form
4. Contact the maintainers

---

**Made with ❤️ for Indian Cinema**

*Preserving and celebrating the rich heritage of Indian films through technology*