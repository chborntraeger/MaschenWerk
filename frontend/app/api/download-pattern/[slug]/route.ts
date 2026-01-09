import { auth } from '@/auth';
import { createAuthenticatedClient } from '@/lib/directus';
import { readItems } from '@directus/sdk';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ slug: string }> }
) {
  try {
    const session = await auth();

    if (!session?.user) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    const { slug } = await params;
    const { client, token } = createAuthenticatedClient(session.user.accessToken);

    // Fetch pattern to verify access and get PDF file ID
    const patterns = await client.request(
      readItems('patterns', {
        filter: {
          slug: { _eq: slug }
        },
        limit: 1
      })
    );

    if (!patterns || patterns.length === 0) {
      return new NextResponse('Pattern not found', { status: 404 });
    }

    const pattern = patterns[0];

    if (!pattern.pdf_file) {
      return new NextResponse('No PDF file found', { status: 404 });
    }

    // Fetch PDF from Directus
    const directusUrl = process.env.NEXT_PUBLIC_DIRECTUS_URL || 'http://localhost:8055';
    const pdfUrl = `${directusUrl}/assets/${pattern.pdf_file}`;

    const pdfResponse = await fetch(pdfUrl, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!pdfResponse.ok) {
      return new NextResponse('Failed to fetch PDF', { status: 500 });
    }

    const pdfBuffer = await pdfResponse.arrayBuffer();

    // Return PDF with appropriate headers
    return new NextResponse(pdfBuffer, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${pattern.slug}.pdf"`,
      },
    });
  } catch (error) {
    console.error('PDF download error:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
