-- ============================================
-- Prmpt - Lessons & Progress Schema
-- ============================================

-- Lessons table (replaces file-based definitions.py)
CREATE TABLE IF NOT EXISTS public.lessons (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    goal TEXT NOT NULL,
    game_type TEXT NOT NULL DEFAULT 'exact_match',
    difficulty TEXT NOT NULL DEFAULT 'beginner',
    order_index INTEGER NOT NULL DEFAULT 0,
    config JSONB NOT NULL DEFAULT '{}',
    time_limit INTEGER, -- seconds, NULL = no timer
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- User progress tracking
CREATE TABLE IF NOT EXISTS public.user_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users (id) ON DELETE CASCADE,
    lesson_id INTEGER REFERENCES public.lessons (id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT false,
    score INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 0,
    completed_at TIMESTAMPTZ,
    UNIQUE (user_id, lesson_id)
);

-- Enable RLS
ALTER TABLE public.lessons ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;

-- Lessons: anyone can read published, admin can manage all
CREATE POLICY "Published lessons are viewable by everyone" ON public.lessons FOR
SELECT USING (is_published = true);

CREATE POLICY "Admins can manage lessons" ON public.lessons FOR ALL USING (
    (
        SELECT raw_user_meta_data ->> 'role'
        FROM auth.users
        WHERE
            id = auth.uid ()
    ) = 'admin'
);

-- User progress: users can manage their own
CREATE POLICY "Users can view own progress" ON public.user_progress FOR
SELECT USING (auth.uid () = user_id);

CREATE POLICY "Users can insert own progress" ON public.user_progress FOR INSERT
WITH
    CHECK (auth.uid () = user_id);

CREATE POLICY "Users can update own progress" ON public.user_progress
FOR UPDATE
    USING (auth.uid () = user_id);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_lessons_order ON public.lessons (order_index);

CREATE INDEX IF NOT EXISTS idx_lessons_published ON public.lessons (is_published);

CREATE INDEX IF NOT EXISTS idx_progress_user ON public.user_progress (user_id);

CREATE INDEX IF NOT EXISTS idx_progress_lesson ON public.user_progress (lesson_id);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER lessons_updated_at
    BEFORE UPDATE ON public.lessons
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- ============================================
-- Seed initial lessons from definitions.py
-- ============================================
INSERT INTO
    public.lessons (
        id,
        title,
        description,
        goal,
        game_type,
        difficulty,
        order_index,
        config,
        is_published
    )
VALUES (
        1,
        'Hello, World!',
        'Your first prompt! Make the AI greet the world.',
        'Write a prompt that makes the AI output exactly: Hello, World!',
        'exact_match',
        'beginner',
        1,
        '{"expected": "Hello, World!", "case_sensitive": true}',
        true
    ),
    (
        2,
        'Count to Five',
        'Numbers are fundamental. Can you count?',
        'Write a prompt that outputs the numbers 1 through 5, separated by commas.',
        'exact_match',
        'beginner',
        2,
        '{"expected": "1, 2, 3, 4, 5", "case_sensitive": true}',
        true
    ),
    (
        3,
        'Reverse It',
        'Sometimes you need to think backwards.',
        'Write a prompt that outputs ''desserts'' (stressed spelled backwards).',
        'exact_match',
        'beginner',
        3,
        '{"expected": "desserts", "case_sensitive": false}',
        true
    ),
    (
        4,
        'JSON Basics',
        'Structured data is powerful. Start with JSON.',
        'Output a valid JSON object with keys ''name'' and ''age''.',
        'exact_match',
        'beginner',
        4,
        '{"expected": "\"name\"", "case_sensitive": true, "match_type": "contains"}',
        true
    ),
    (
        5,
        'The Polite AI',
        'Manners matter, even for AI.',
        'Make the AI say ''Please'' and ''Thank you'' in the same response.',
        'exact_match',
        'intermediate',
        5,
        '{"expected": "(?i)please.*thank you|thank you.*please", "case_sensitive": false, "match_type": "regex"}',
        true
    ),

-- New game type examples
(
    6,
    'Prompt Building Blocks',
    'Learn the key components of a good prompt.',
    'Fill in the blanks to complete this effective prompt template.',
    'fill_blank',
    'beginner',
    6,
    '{"template": "Act as a {{blank}}. I want you to {{blank}} about {{blank}}.", "answers": ["expert", "explain", "AI"], "case_sensitive": false}',
    true
),
(
    7,
    'Which Prompt Wins?',
    'Not all prompts are created equal. Pick the best one!',
    'Select the most effective prompt for getting a concise summary.',
    'multiple_choice',
    'beginner',
    7,
    '{"question": "Which prompt will give you the best concise summary of a long article?", "options": ["Summarize this", "Please read and provide a 3-sentence summary focusing on key takeaways", "Tell me about this article", "What does this say?"], "correct": [1], "multi": false}',
    true
),
(
    8,
    'Order of Operations',
    'The order of instructions in a prompt matters!',
    'Arrange these prompt components in the most effective order.',
    'reorder',
    'intermediate',
    8,
    '{"items": ["Define the role", "Provide context", "Give specific instructions", "Specify output format"], "correct_order": [0, 1, 2, 3]}',
    true
);

-- Reset sequence
SELECT setval( 'lessons_id_seq', ( SELECT MAX(id) FROM lessons ) );